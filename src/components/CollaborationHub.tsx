import React, { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';

interface Message {
  user: string;
  text: string;
}

const CollaborationHub: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState('');
  const socketRef = useRef<Socket | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const user = 'anonymous';

  useEffect(() => {
    fetch('/api/collaboration/chat?limit=200')
      .then((res) => res.json())
      .then((data) => setMessages(data));

    const socket = io('/ws');
    socketRef.current = socket;
    socket.on('message', (msg: Message) => {
      setMessages((prev) => [...prev, msg].slice(-200));
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = () => {
    if (!text.trim()) return;
    socketRef.current?.emit('message', { user, text });
    setText('');
  };

  return (
    <div>
      <div style={{ height: '300px', overflowY: 'auto', border: '1px solid #ccc', padding: '0.5rem' }}>
        {messages.map((m, idx) => (
          <div key={idx}>
            <strong>{m.user}:</strong> {m.text}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') sendMessage();
        }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default CollaborationHub;
