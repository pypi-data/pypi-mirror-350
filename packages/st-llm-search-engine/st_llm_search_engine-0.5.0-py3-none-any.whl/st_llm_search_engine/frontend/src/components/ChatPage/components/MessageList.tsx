import React, { useRef, useEffect } from 'react';
import { MessageListProps } from '../types';
import MessageItem from './MessageItem';
import ThinkingIndicator from './ThinkingIndicator';
import ErrorMessage from './ErrorMessage';
import WelcomeMessage from './WelcomeMessage';

const MessageList: React.FC<MessageListProps> = ({
  messages,
  isThinking,
  error,
  searchId,
  onErrorClear
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  // 滾動到底部
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isThinking]);

  const showWelcome = searchId === "999" && messages.length === 0 && !isThinking;

  return (
    <div
      style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        padding: '24px 0',
        paddingBottom: '80px',
        background: '#222',
        height: '100%',
        width: '100%',
        position: 'relative'
      }}
    >
      <WelcomeMessage isVisible={showWelcome} />

      <div style={{
        width: '80%',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        visibility: showWelcome ? 'hidden' : 'visible'
      }}>
        {messages.map((message) => (
          <MessageItem
            key={message.id}
            message={message}
            isUser={message.role === 'user'}
          />
        ))}

        <ThinkingIndicator isVisible={isThinking} />

        <ErrorMessage
          message={error}
          onClear={onErrorClear}
          isVisible={!!error}
        />

        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default MessageList;
