import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.rtcconfiguration import RTCConfiguration, RTCIceServer
import socketio
from datetime import datetime
from typing import Optional, Callable, Dict, Any, List
from lzstring import LZString
import uuid
import base64

class RoboticsClient:
    def __init__(self):
        self._pc: Optional[RTCPeerConnection] = None
        self._channels: Dict[int, Any] = {}  # Map to store multiple data channels
        self._current_channel_index = 0
        self._num_channels = 10  # Default number of data channels
        self._sio = None
        self._connected = False
        self._callback = None
        self._robot_id = None
        self._token = None
        self._pending_messages = []
        self.lzstring = LZString()
        self.messages = {}
        self._setup_complete = False
        self._setup_in_progress = False
        self._has_remote_description = False
        self._pending_candidates = []
        self._max_message_size = 16384  # Match JavaScript maxMessageSize
        self._port_range_begin = 5000  # Match JavaScript portRangeBegin
        self._port_range_end = 6000  # Match JavaScript portRangeEnd
        self._channel_recreation_times = {}  # Track when channels were last recreated
        self._min_recreation_delay = 5  # Minimum seconds between recreations

    def _get_next_channel(self) -> Optional[Any]:
        """Get next available channel in round-robin fashion"""
        if not self._channels:
            return None
        channel = self._channels.get(self._current_channel_index)
        self._current_channel_index = (self._current_channel_index + 1) % self._num_channels
        return channel

    async def _send_compressed_message(self, message: Dict[str, Any]) -> None:
        """Send compressed message through available channels"""
        try:
            print(f"\n=== Sending Compressed Message ===")
            print(f"Message: {json.dumps(message, indent=2)}")
            
            # Validate message format
            if not isinstance(message, dict):
                print("ERROR: Message must be a dictionary")
                return
                
            # Check for P2P message format
            if 'type' in message:
                print(f"Sending P2P message of type: {message['type']}")
            else:
                # Validate ROS message format
                if 'topic' not in message:
                    print("ERROR: Message must have a topic")
                    return
                    
                if message['topic'] == 'speak' and not isinstance(message.get('text'), str):
                    print("ERROR: Speak message must have text as string")
                    return
                    
                if message['topic'] == 'twist' and not isinstance(message.get('twist'), dict):
                    print("ERROR: Twist message must have twist as dictionary")
                    return
            
            # Compress message exactly like JavaScript
            compressed = self.lzstring.compressToBase64(json.dumps(message))
            message_id = str(uuid.uuid4())
            chunk_size = self._max_message_size
            total_chunks = (len(compressed) + chunk_size - 1) // chunk_size

            # Get all open channels
            open_channels = [
                channel for channel in self._channels.values()
                if channel and channel.readyState == "open"
            ]
            
            print(f"Open channels: {len(open_channels)}")
            print(f"Channel states: {[(i, ch.readyState) for i, ch in self._channels.items()]}")
            
            if not open_channels:
                print("No open channels available")
                self._pending_messages.append(message)
                return

            print(f"Sending {total_chunks} chunks for message {message_id}")
            print(f"Total channels available: {len(open_channels)}")

            # Distribute chunks across all available channels
            for i in range(total_chunks):
                chunk = compressed[i * chunk_size:(i + 1) * chunk_size]
                # Create message chunk format to match JavaScript exactly
                message_chunk = {
                    'chunk': chunk,
                    'index': i,
                    'total': total_chunks,
                    'messageId': message_id
                }
                
                # Select channel based on chunk index
                channel_index = i % len(open_channels)
                channel = open_channels[channel_index]
                
                try:
                    print(f"Sending chunk {i + 1}/{total_chunks} on channel {channel.label}")
                    print(f"Channel state: {channel.readyState}")
                    # Create message chunk format to match JavaScript exactly
                    message_chunk = {
                        'chunk': chunk,
                        'index': i,
                        'total': total_chunks,
                        'messageId': message_id
                    }
                    # Send as string that can be parsed by JSON.parse()
                    message_str = json.dumps(message_chunk)
                    print(f"Sending message: {message_str}")
                    channel.send(message_str)
                    print(f"Successfully sent chunk {i + 1}/{total_chunks}")
                except Exception as e:
                    print(f"Error sending chunk {i + 1}/{total_chunks} on channel {channel.label}: {e}")
                    self._pending_messages.append(message_chunk)

        except Exception as e:
            print(f"Error sending compressed message: {e}")
            self._pending_messages.append(message)

    async def _setup_peer_connection(self):
        """Set up WebRTC peer connection with multiple data channels"""
        if self._setup_in_progress:
            print("Setup already in progress, skipping...")
            return
        
        self._setup_in_progress = True
        print("\n=== Setting up Peer Connection ===")
        print(f"Current connection state: {self._pc.connectionState if self._pc else 'No PC'}")
        print(f"Current ICE connection state: {self._pc.iceConnectionState if self._pc else 'No PC'}")
        
        try:
            if self._pc:
                print("Closing existing peer connection...")
                await self._pc.close()
                self._pc = None

            # Match JavaScript configuration
            config = RTCConfiguration([
                RTCIceServer(urls=["stun:stun1.l.google.com:19302"]),
                RTCIceServer(urls=["stun:stun2.l.google.com:19302"])
            ])
            
            # Set port range and max message size
            config.portRangeBegin = self._port_range_begin
            config.portRangeEnd = self._port_range_end
            config.maxMessageSize = self._max_message_size
            
            print("Creating new peer connection...")
            self._pc = RTCPeerConnection(configuration=config)

            @self._pc.on("connectionstatechange")
            async def on_connectionstatechange():
                print(f"\n=== Connection State Changed ===")
                print(f"New state: {self._pc.connectionState}")
                print(f"ICE connection state: {self._pc.iceConnectionState}")
                print(f"ICE gathering state: {self._pc.iceGatheringState}")
                if self._pc.connectionState == "connected":
                    print("Peer connection established!")
                    self._connected = True
                    self._setup_complete = True
                    self._setup_in_progress = False
                    print(f"Active data channels: {[(i, ch.readyState) for i, ch in self._channels.items()]}")
                    open_channels = [ch for ch in self._channels.values() if ch and ch.readyState == "open"]
                    print(f"Total open channels: {len(open_channels)}/{self._num_channels}")
                    if len(open_channels) == 0:
                        print("WARNING: No open channels after connection established!")

            @self._pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                print(f"\n=== ICE Connection State Changed ===")
                print(f"New state: {self._pc.iceConnectionState}")

            @self._pc.on("icegatheringstatechange")
            async def on_icegatheringstatechange():
                print(f"\n=== ICE Gathering State Changed ===")
                print(f"New state: {self._pc.iceGatheringState}")

            # Create data channels
            print("\n=== Creating Data Channels ===")
            for i in range(self._num_channels):
                try:
                    channel = self._pc.createDataChannel(
                        f'robotics-{i}',
                        ordered=True,
                        protocol='chat'
                    )
                    self._channels[i] = channel
                    print(f"Created data channel {i}: {channel.label}")
                    print(f"Channel ID: {channel.id}")
                    print(f"Initial State: {channel.readyState}")
                    self._setup_data_channel(channel)
                except Exception as e:
                    print(f"Error creating data channel {i}: {e}")
                    raise e

            # Create and send offer
            print("\n=== Creating Offer ===")
            offer = await self._pc.createOffer()
            await self._pc.setLocalDescription(offer)

            # Format SDP for compatibility
            sdp_lines = []
            ice_lines = []
            fingerprint = None

            # Extract components from original SDP
            for line in offer.sdp.split('\r\n'):
                if line.startswith('a=ice-ufrag:'):
                    ice_lines.append(line)
                elif line.startswith('a=ice-pwd:'):
                    ice_lines.append(line)
                elif line.startswith('a=fingerprint:sha-256'):
                    fingerprint = line

            # Build SDP with exact format
            sdp_lines = [
                'v=0',
                f'o=- {int(datetime.now().timestamp())} 1 IN IP4 0.0.0.0',
                's=-',
                't=0 0',
                'm=application 9 UDP/DTLS/SCTP webrtc-datachannel',
                'c=IN IP4 0.0.0.0',
                'a=mid:0'
            ]

            # Add ICE and fingerprint in correct order
            sdp_lines.extend(ice_lines)
            if fingerprint:
                sdp_lines.append(fingerprint)

            # Add required attributes
            sdp_lines.extend([
                'a=sctp-port:5000',
                'a=max-message-size:262144',
                'a=setup:actpass'
            ])

            modified_sdp = '\r\n'.join(sdp_lines) + '\r\n'

            # Send offer
            print("\n=== Sending Offer ===")
            await self._sio.emit('signal', {
                'type': 'offer',
                'robot': self._robot_id,
                'token': self._token,
                'targetPeer': self._robot_id,
                'sourcePeer': self._client_id,
                'room': self._robot_id,
                'sdp': modified_sdp
            })
            print("Sent offer to peer")

            @self._pc.on("icecandidate")
            async def on_icecandidate(candidate):
                if candidate:
                    print(f"\n=== ICE Candidate ===")
                    print(f"Candidate: {candidate.candidate}")
                    await self._sio.emit('signal', {
                        'type': 'candidate',
                        'robot': self._robot_id,
                        'token': self._token,
                        'targetPeer': self._robot_id,
                        'sourcePeer': self._client_id,
                        'room': self._robot_id,
                        'candidate': candidate.candidate,
                        'mid': candidate.sdpMid
                    })

        except Exception as e:
            print(f"Setup failed: {e}")
            self._setup_in_progress = False
            raise e

    async def _handle_peer_reply(self, data):
        """Handle peer connection signaling"""
        try:
            print(f"\n=== Handling Peer Reply ===")
            print(f"Type: {data.get('type')}")
            
            if data['type'] == 'answer':
                # Convert answer SDP for aiortc
                sdp = data['sdp'].replace(
                    'UDP/DTLS/SCTP webrtc-datachannel',
                    'DTLS/SCTP 5000'
                )
                answer = RTCSessionDescription(sdp=sdp, type='answer')
                await self._pc.setRemoteDescription(answer)
                self._has_remote_description = True
                print("Set remote description")
                
                # Process any pending candidates
                while self._pending_candidates:
                    candidate = self._pending_candidates.pop(0)
                    await self._pc.addIceCandidate(candidate)
                    print(f"Added pending ICE candidate: {candidate.candidate}")
                
                # Check data channel states after setting remote description
                print("\n=== Data Channel States After Answer ===")
                for i, channel in self._channels.items():
                    print(f"Channel {i}: {channel.readyState}")
                
                # Wait a bit for channels to open
                await asyncio.sleep(1)
                
                # Check channel states again
                print("\n=== Data Channel States After Delay ===")
                open_channels = []
                for i, channel in self._channels.items():
                    print(f"Channel {i}: {channel.readyState}")
                    if channel.readyState == "open":
                        open_channels.append(channel)
                    else:
                        # Only recreate if enough time has passed
                        current_time = datetime.now().timestamp()
                        last_recreation = self._channel_recreation_times.get(i, 0)
                        if current_time - last_recreation >= self._min_recreation_delay:
                            print(f"Attempting to reopen channel {i}")
                            try:
                                new_channel = self._pc.createDataChannel(
                                    f'robotics-{i}',
                                    ordered=True,
                                    protocol='chat'
                                )
                                self._channels[i] = new_channel
                                self._setup_data_channel(new_channel)
                                self._channel_recreation_times[i] = current_time
                                print(f"Recreated channel {i}")
                                if new_channel.readyState == "open":
                                    open_channels.append(new_channel)
                            except Exception as e:
                                print(f"Error recreating channel {i}: {e}")
            
            elif data['type'] == 'candidate':
                try:
                    # Handle candidate string directly
                    raw = data.get('candidate', '')
                    if raw.startswith('a='):
                        raw = raw[2:]
                    if raw.startswith('candidate:'):
                        raw = raw[10:]
                    
                    # Parse the candidate string
                    parts = raw.split()
                    if len(parts) >= 8:
                        # Create candidate with parsed components
                        candidate = RTCIceCandidate(
                            component=1,
                            foundation=parts[0],
                            protocol=parts[2].lower(),
                            priority=int(parts[3]),
                            ip=parts[4],
                            port=int(parts[5]),
                            type=parts[7],
                            sdpMid=data.get('mid', '0'),
                            sdpMLineIndex=0
                        )
                        
                        if not self._has_remote_description:
                            self._pending_candidates.append(candidate)
                            print(f"Queued ICE candidate: {raw}")
                        else:
                            await self._pc.addIceCandidate(candidate)
                            print(f"Added ICE candidate: {raw}")
                except Exception as e:
                    print(f"ICE candidate error: {str(e)}")
                    print(f"Raw candidate data: {data}")

        except Exception as e:
            print(f"Peer reply error: {str(e)}")
            print(f"Full data: {data}")

    def _convert_compressed_image_to_base64(self, image_data):
        """Convert compressed image data to base64 string"""
        try:
            # Handle different possible data structures
            compressed_data = None
            if isinstance(image_data, list):
                compressed_data = image_data
            elif isinstance(image_data, dict):
                if isinstance(image_data.get('data'), list):
                    compressed_data = image_data['data']
                elif isinstance(image_data.get('buffer'), (list, bytes)):
                    compressed_data = image_data['buffer']
                elif isinstance(image_data.get('data'), dict):
                    # Handle the case where data is an object with numeric keys
                    data_obj = image_data['data']
                    # Convert numeric-keyed object to array
                    compressed_data = [data_obj[str(i)] for i in range(len(data_obj))]
                else:
                    print("Unsupported image data format")
                    return None
            else:
                print("Unsupported image data format")
                return None

            if not compressed_data or len(compressed_data) == 0:
                print("No valid image data found")
                return None
            
            # Convert the array to bytes
            buffer = bytes(compressed_data)
            
            # Convert bytes to base64
            base64_str = base64.b64encode(buffer).decode('utf-8')
            
            # Validate the base64 string
            if len(base64_str) < 100:  # Arbitrary minimum length for a valid image
                print("Generated base64 string too short, likely invalid")
                return None
            
            return base64_str
        except Exception as e:
            print(f"Error converting compressed image: {e}")
            return None

    def _setup_data_channel(self, channel):
        """Set up data channel handlers"""
        if not channel:
            print("No channel provided to setup")
            return

        @channel.on("open")
        def on_open():
            print(f"\n=== Data Channel {channel.label} Opened ===")
            print(f"Channel ID: {channel.id}")
            print(f"Channel Protocol: {channel.protocol}")
            print(f"Channel State: {channel.readyState}")
            print(f"Peer Connection State: {self._pc.connectionState if self._pc else 'No PC'}")
            print(f"ICE Connection State: {self._pc.iceConnectionState if self._pc else 'No PC'}")
            
            # Only send ready signal if peer connection is connected
            if self._pc and self._pc.connectionState == "connected":
                # Send ready signal
                ready_msg = json.dumps({
                    "type": "ready",
                    "channel": channel.id,
                    "total_channels": self._num_channels
                })
                print(f"Sending ready signal on channel {channel.id}: {ready_msg}")
                try:
                    # Send as string that can be parsed by JSON.parse()
                    channel.send(ready_msg)
                    print(f"Successfully sent ready signal on channel {channel.id}")
                except Exception as e:
                    print(f"Error sending ready signal on channel {channel.id}: {e}")
                    return
                
                # Execute callback
                if self._callback:
                    print(f"Executing connected callback for channel {channel.id}")
                    asyncio.create_task(self._callback({"type": "connected", "channel": channel.id}))
            else:
                print(f"Not sending ready signal - peer connection not ready: {self._pc.connectionState if self._pc else 'No PC'}")

        @channel.on("message")
        def on_message(message):
            if not self._callback:
                return
                
            if not isinstance(message, str):
                return

            try:
                # Parse the message
                data = json.loads(message)
                
                # Check if this is a chunked message
                if all(k in data for k in ['chunk', 'index', 'total', 'messageId']):
                    message_id = data['messageId']
                    if message_id not in self.messages:
                        self.messages[message_id] = {
                            'chunks': [None] * data['total'],
                            'total': data['total'],
                            'received': 0,
                            'topic': data.get('topic')  # Store topic from first chunk
                        }
                    
                    # Store this chunk
                    if self.messages[message_id]['chunks'][data['index']] is None:
                        self.messages[message_id]['chunks'][data['index']] = data['chunk']
                        self.messages[message_id]['received'] += 1
                    
                    # Check if we have all chunks
                    if self.messages[message_id]['received'] == data['total']:
                        # Combine and decompress exactly like JavaScript
                        combined = ''.join(self.messages[message_id]['chunks'])
                        try:
                            # First decompress, then parse JSON
                            decompressed = self.lzstring.decompressFromBase64(combined)
                            if decompressed:
                                result = json.loads(decompressed)
                                # print(f"\n=== Decompressed Message ===")
                                # print(f"Data: {json.dumps(result, indent=2)}")
                                
                                # Handle different message formats
                                if isinstance(result, dict):
                                    # Check for P2P message format
                                    if 'type' in result:
                                        print(f"P2P message type: {result['type']}")
                                        del self.messages[message_id]
                                        asyncio.create_task(self._callback(result))
                                        return
                                        
                                    # Check for ROS message format
                                    if 'topic' in result:
                                        print(f"P2P message type: {result['topic']}")
                                        topic = result['topic']
                                    elif 'header' in result and 'frame_id' in result['header']:
                                        topic = result['header']['frame_id']
                                    else:
                                        topic = None
                                        
                                    # Create proper ROS message format
                                    ros_message = {
                                        'topic': topic,
                                        'data': result
                                    }
                                    
                                    # Handle compressed image messages
                                    if topic == '/camera/camera/color/image_raw/compressed':
                                        try:
                                            # Get the compressed image data
                                            if 'data' in result:
                                                base64_image = self._convert_compressed_image_to_base64(result['data'])
                                                if base64_image:
                                                    ros_message['data']['base64Image'] = base64_image
                                                    # print(f"Added base64 image to compressed image message")
                                        except Exception as e:
                                            print(f"Error handling compressed image: {e}")
                                    
                                    # Validate message format
                                    if topic == 'speak':
                                        if not isinstance(result.get('text'), str):
                                            print(f"ERROR: Invalid speak message format - text must be string")
                                            return
                                        # Create speak message
                                        speak_message = {
                                            'type': 'speak',
                                            'text': result['text']
                                        }
                                        del self.messages[message_id]
                                        # print(f"Calling callback with speak message")
                                        asyncio.create_task(self._callback(speak_message))
                                    else:
                                        del self.messages[message_id]
                                        # print(f"Calling callback with ROS message")
                                        asyncio.create_task(self._callback(ros_message))
                                else:
                                    print(f"ERROR: Invalid message format - expected dictionary")
                                    return
                            else:
                                print(f"\n=== Decompression Failed - Using Raw Message ===")
                                result = json.loads(combined)
                                print(f"Data: {json.dumps(result, indent=2)}")
                                del self.messages[message_id]
                                asyncio.create_task(self._callback(result))
                        except Exception as e:
                            print(f"\n=== Message Processing Error ===")
                            print(f"Error: {str(e)}")
                            print(f"Raw message: {combined[:200]}...")
                            return
                else:
                    # Handle regular messages
                    # print(f"\n=== Regular Message ===")
                    # print(f"Raw data: {json.dumps(data, indent=2)}")
                    
                    # Check for P2P message format
                    if isinstance(data, dict) and 'type' in data:
                        print(f"P2P message type: {data['type']}")
                        asyncio.create_task(self._callback(data))
                        return
                        
                    # Handle ROS message format
                    if isinstance(data, dict):
                        if 'topic' in data:
                            topic = data['topic']
                        elif 'header' in data and 'frame_id' in data['header']:
                            topic = data['header']['frame_id']
                        else:
                            topic = None
                            
                        # Create proper ROS message format
                        ros_message = {
                            'topic': topic,
                            'data': data
                        }

                        # Handle compressed image messages
                        if topic == '/camera/camera/color/image_raw/compressed':
                            try:
                                # Get the compressed image data
                                if 'data' in data:
                                    base64_image = self._convert_compressed_image_to_base64(data['data'])
                                    if base64_image:
                                        ros_message['data']['base64Image'] = base64_image
                                        # print(f"Added base64 image to compressed image message")
                            except Exception as e:
                                print(f"Error handling compressed image: {e}")
                            
                        # print(f"Formatted ROS message: {json.dumps(ros_message, indent=2)}")
                        asyncio.create_task(self._callback(ros_message))
                    else:
                        print(f"ERROR: Invalid message format - expected dictionary")
                        return
            except Exception as e:
                print(f"\n=== Message Handling Error ===")
                print(f"Error: {str(e)}")
                print(f"Raw message: {message[:200]}...")
                return

        @channel.on("error")
        def on_error(error):
            print(f"\n=== Data Channel {channel.label} Error ===")
            print(f"Channel ID: {channel.id}")
            print(f"Error: {error}")
            self._connected = False

        @channel.on("close")
        def on_close():
            print(f"\n=== Data Channel {channel.label} Closed ===")
            print(f"Channel ID: {channel.id}")
            self._connected = False

    async def disconnect(self) -> None:
        """Clean shutdown of connections"""
        for channel in self._channels.values():
            if channel:
                channel.close()
        self._channels.clear()
        if self._pc:
            await self._pc.close()
        if self._sio:
            await self._sio.disconnect()
        self._connected = False

    async def connect(self, options: Dict[str, str], callback: Callable[[Dict], None]) -> None:
        """Connect to robotics.dev and establish P2P connection"""
        self._callback = callback
        self._robot_id = options.get('robot')
        self._token = options.get('token')
        
        # Ensure server URL is properly handled
        server = options.get('server')
        if not server:
            server = 'wss://robotics.dev'
        elif server.startswith('http://'):
            server = server.replace('http://', 'ws://')
        elif server.startswith('https://'):
            server = server.replace('https://', 'wss://')
        elif not server.startswith(('ws://', 'wss://')):
            server = f"ws://{server}"
            
        self._server = server
        print(f"Using signaling server: {self._server}")

        if not self._robot_id or not self._token:
            raise ValueError("Both robot ID and token are required")

        # Initialize socket.io with debugging
        self._sio = socketio.AsyncClient(logger=True, engineio_logger=True)
        self._client_id = f'remote-{hex(int(datetime.now().timestamp()))[2:]}'

        @self._sio.event
        async def connect():
            print(f"Connected to signaling server: {self._server}")
            print(f"Client ID: {self._client_id}")
            # Emit register event first
            await self._sio.emit('register', {
                'id': self._client_id,
                'room': self._robot_id,
                'token': self._token
            })
            # Then emit join signal
            await self._sio.emit('signal', {
                'type': 'join',
                'robot': self._robot_id,
                'token': self._token,
                'targetPeer': self._robot_id,
                'sourcePeer': self._client_id,
                'room': self._robot_id  # Add room parameter
            })
            # Set up peer connection immediately after registering
            await self._setup_peer_connection()

        @self._sio.event
        async def disconnect():
            print("Disconnected from signaling server")

        @self._sio.event
        async def error(data):
            print(f"Socket.IO error: {data}")

        @self._sio.event
        async def signal(data):
            print(f"Received signal: {data.get('type')}")
            if data.get('type') in ['answer', 'candidate']:
                await self._handle_peer_reply(data)

        @self._sio.event
        async def room_info(info):
            print(f"Received room info: {info}")
            if info.get('peers') and self._robot_id in info['peers'] and not self._connected and not self._setup_complete:
                await self._setup_peer_connection()

        # Connect with proper URL parameters
        connection_url = (
            f"{self._server}?"
            f"id={self._client_id}&"
            f"room={self._robot_id}&"  # Add room parameter
            f"token={self._token}"
        )
        
        print(f"Connecting to: {connection_url}")
        await self._sio.connect(
            connection_url,
            transports=["websocket"],
            auth={'id': self._client_id}  # Add auth parameter
        )

        # Keep the connection alive and wait for messages
        while True:
            try:
                await asyncio.sleep(1)
                # Check if we have any open channels
                open_channels = [ch for ch in self._channels.values() if ch and ch.readyState == "open"]
                if not open_channels and self._connected:
                    print("No open channels, attempting to reconnect...")
                    await self._setup_peer_connection()
            except Exception as e:
                print(f"Error in connection loop: {e}")
                break

    async def twist(self, robot: str, twist_msg: Dict[str, Any]) -> None:
        """Send twist command to robot"""
        print(f"\n=== Sending Twist Command ===")
        print(f"Robot: {robot}")
        print(f"Twist message: {json.dumps(twist_msg, indent=2)}")
        
        # Validate twist message format
        if not isinstance(twist_msg, dict):
            print("ERROR: Twist message must be a dictionary")
            return
            
        # Create message format to match robotics.js exactly
        message = {
            'topic': 'twist',
            'robot': robot,
            'twist': twist_msg
        }
        print(f"Twist message format: {json.dumps(message, indent=2)}")
        await self._send_message(message)

    async def speak(self, robot: str, text: str) -> None:
        """Send speak command to robot"""
        print(f"\n=== Sending Speak Command ===")
        print(f"Robot: {robot}")
        print(f"Text: {text}")
        
        # Validate text format
        if not isinstance(text, str):
            print("ERROR: Text must be a string")
            return
            
        # Create message format to match robotics.js exactly
        message = {
            'topic': 'speak',
            'robot': robot,
            'text': text
        }
        print(f"Speak message format: {json.dumps(message, indent=2)}")
        await self._send_message(message)

    async def _send_message(self, message: Dict[str, Any]) -> None:
        """Send message through data channel or queue if not connected"""
        try:
            print(f"\n=== Sending Message ===")
            print(f"Connected: {self._connected}")
            print(f"Message: {message}")
            
            # Wait for connection to be established
            max_wait = 10  # Maximum seconds to wait
            start_time = datetime.now().timestamp()
            while not self._connected or not self._pc or self._pc.connectionState != "connected":
                if datetime.now().timestamp() - start_time > max_wait:
                    print("Timeout waiting for connection")
                    self._pending_messages.append(message)
                    return
                print("Waiting for connection to be established...")
                await asyncio.sleep(0.5)
            
            # Wait for at least one channel to be open
            while not any(ch and ch.readyState == "open" for ch in self._channels.values()):
                if datetime.now().timestamp() - start_time > max_wait:
                    print("Timeout waiting for open channel")
                    self._pending_messages.append(message)
                    return
                print("Waiting for channel to open...")
                await asyncio.sleep(0.5)
            
            if self._connected:
                print("Sending through data channel...")
                # For speak and twist messages, send directly without compression
                if message.get('topic') in ['speak', 'twist']:
                    # Get an open channel
                    open_channels = [ch for ch in self._channels.values() if ch and ch.readyState == "open"]
                    if open_channels:
                        channel = open_channels[0]  # Use first open channel
                        try:
                            print(f"Sending direct message on channel {channel.label}")
                            print(f"Channel state: {channel.readyState}")
                            message_str = json.dumps(message)
                            print(f"Sending message: {message_str}")
                            channel.send(message_str)
                            print(f"Successfully sent direct message")
                        except Exception as e:
                            print(f"Error sending direct message on channel {channel.label}: {e}")
                            self._pending_messages.append(message)
                    else:
                        print("No open channels available")
                        self._pending_messages.append(message)
                else:
                    # For other messages, use compression
                    await self._send_compressed_message(message)
            else:
                print("Not connected, queueing message")
                self._pending_messages.append(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self._pending_messages.append(message)

# Create singleton instance
robotics = RoboticsClient()
