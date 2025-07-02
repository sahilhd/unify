import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useUsageStats } from './Analytics';
import { 
  PaperAirplaneIcon,
  UserIcon,
  SparklesIcon,
  ChevronDownIcon,
  TrashIcon
} from '@heroicons/react/24/outline';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  model?: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  model: string;
  lastUpdated: Date;
}

const models = [
  { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', provider: 'OpenAI', description: 'Fast and efficient for most tasks' },
  { id: 'gpt-4', name: 'GPT-4', provider: 'OpenAI', description: 'Most capable model for complex reasoning' },
  { id: 'claude-3-opus-20240229', name: 'Claude 3 Opus', provider: 'Anthropic', description: 'Most capable Claude model' },
  { id: 'claude-3-haiku-20240307', name: 'Claude 3 Haiku', provider: 'Anthropic', description: 'Fastest Claude model, great for low-latency tasks' },
  // { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet', provider: 'Anthropic', description: 'Balanced performance and speed (not available)' },
  // { id: 'claude-2.1', name: 'Claude 2.1', provider: 'Anthropic', description: 'Legacy Claude model (not available)' },
  { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', description: 'Google\'s most capable model' },
];

const MAX_CHAT_SESSIONS = 10;

const getChatStorageKey = () => {
  const apiKey = localStorage.getItem('unillm_api_key');
  return apiKey ? `unillm_chat_history_${apiKey}` : 'unillm_chat_history';
};

const Chat: React.FC = () => {
  const { user } = useAuth();
  const { refreshUsageStats } = useUsageStats();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedModel, setSelectedModel] = useState(models[0]);
  const [isLoading, setIsLoading] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string>('');
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load chat history from localStorage on component mount and when user changes
  useEffect(() => {
    loadChatHistory();
  }, [user]);

  // Save messages to localStorage whenever messages change
  useEffect(() => {
    if (messages.length > 0) {
      saveCurrentSession();
    }
  }, [messages]);

  const loadChatHistory = () => {
    try {
      const saved = localStorage.getItem(getChatStorageKey());
      if (saved) {
        const sessions: ChatSession[] = JSON.parse(saved);
        
        // Convert timestamp strings back to Date objects
        const processedSessions = sessions.map(session => ({
          ...session,
          messages: session.messages.map(message => ({
            ...message,
            timestamp: new Date(message.timestamp)
          })),
          lastUpdated: new Date(session.lastUpdated)
        }));
        
        setChatSessions(processedSessions);
        
        // Load the most recent session if no current session
        if (processedSessions.length > 0 && !currentSessionId) {
          const latestSession = processedSessions[0];
          setCurrentSessionId(latestSession.id);
          setMessages(latestSession.messages);
          setSelectedModel(models.find(m => m.id === latestSession.model) || models[0]);
        }
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const saveCurrentSession = () => {
    if (messages.length === 0) return;

    try {
      const title = messages[0]?.content.slice(0, 50) + (messages[0]?.content.length > 50 ? '...' : '');
      const session: ChatSession = {
        id: currentSessionId || Date.now().toString(),
        title,
        messages: [...messages],
        model: selectedModel.id,
        lastUpdated: new Date(),
      };

      let updatedSessions = [...chatSessions];
      
      // Update existing session or add new one
      const existingIndex = updatedSessions.findIndex(s => s.id === session.id);
      if (existingIndex >= 0) {
        updatedSessions[existingIndex] = session;
      } else {
        updatedSessions.unshift(session);
        // Remove oldest session if we exceed the limit
        if (updatedSessions.length > MAX_CHAT_SESSIONS) {
          updatedSessions = updatedSessions.slice(0, MAX_CHAT_SESSIONS);
        }
      }

      // Sort by last updated (most recent first)
      updatedSessions.sort((a, b) => new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime());
      
      setChatSessions(updatedSessions);
      setCurrentSessionId(session.id);
      localStorage.setItem(getChatStorageKey(), JSON.stringify(updatedSessions));
    } catch (error) {
      console.error('Error saving chat session:', error);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setCurrentSessionId('');
    setInputMessage('');
  };

  const loadSession = (session: ChatSession) => {
    // Ensure timestamps are Date objects
    const processedMessages = session.messages.map(message => ({
      ...message,
      timestamp: new Date(message.timestamp)
    }));
    
    setMessages(processedMessages);
    setCurrentSessionId(session.id);
    setSelectedModel(models.find(m => m.id === session.model) || models[0]);
  };

  const deleteSession = (sessionId: string) => {
    const updatedSessions = chatSessions.filter(s => s.id !== sessionId);
    setChatSessions(updatedSessions);
    localStorage.setItem(getChatStorageKey(), JSON.stringify(updatedSessions));
    
    // If we deleted the current session, start a new one
    if (sessionId === currentSessionId) {
      startNewChat();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const apiKey = localStorage.getItem('unillm_api_key');
      
      // Build conversation history for the API request
      const conversationHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));
      
      // Add the current message to the conversation
      conversationHistory.push({
        role: 'user',
        content: inputMessage
      });

      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: selectedModel.id,
          messages: conversationHistory,
          temperature: 0.7,
          max_tokens: 1000,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Chat response:', data);
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          timestamp: new Date(),
          model: selectedModel.id,
        };
        setMessages(prev => [...prev, assistantMessage]);
        
        // Refresh usage stats after successful chat
        refreshUsageStats();
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Chat error:', errorData);
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `Sorry, I encountered an error: ${errorData.detail || 'Unknown error'}`,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Chat</h1>
            <p className="text-gray-400">Interact with AI models through a unified interface</p>
          </div>
          
          {/* New Chat Button */}
          <button
            onClick={startNewChat}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            New Chat
          </button>
        </div>
        
        {/* Model Selector */}
        <div className="relative">
          <button
            onClick={() => setShowModelDropdown(!showModelDropdown)}
            className="flex items-center space-x-2 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white hover:bg-gray-700 transition-colors"
          >
            <SparklesIcon className="h-5 w-5" />
            <span>{selectedModel.name}</span>
            <ChevronDownIcon className="h-4 w-4" />
          </button>
          
          {showModelDropdown && (
            <div className="absolute right-0 mt-2 w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg z-10">
              <div className="p-2">
                {models.map((model) => (
                  <button
                    key={model.id}
                    onClick={() => {
                      setSelectedModel(model);
                      setShowModelDropdown(false);
                    }}
                    className="w-full text-left p-3 rounded-md hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white font-medium">{model.name}</div>
                        <div className="text-sm text-gray-400">{model.description}</div>
                      </div>
                      <div className="text-xs text-gray-500 bg-gray-700 px-2 py-1 rounded">
                        {model.provider}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Chat History Sidebar and Messages */}
      <div className="flex flex-1 gap-4">
        {/* Chat History Sidebar */}
        <div className="w-64 bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-lg font-semibold text-white mb-4">Chat History</h3>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {chatSessions.length === 0 ? (
              <p className="text-gray-400 text-sm">No chat history yet</p>
            ) : (
              chatSessions.map((session) => (
                <div
                  key={session.id}
                  className={`p-3 rounded-lg cursor-pointer transition-colors ${
                    session.id === currentSessionId
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => loadSession(session)}
                      className="flex-1 text-left truncate"
                    >
                      <div className="text-sm font-medium truncate">{session.title}</div>
                      <div className="text-xs opacity-70">
                        {new Date(session.lastUpdated).toLocaleDateString()}
                      </div>
                    </button>
                    <button
                      onClick={() => deleteSession(session.id)}
                      className="ml-2 p-1 hover:bg-red-600 rounded transition-colors"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <SparklesIcon className="mx-auto h-12 w-12 text-gray-500" />
                <h3 className="mt-2 text-sm font-medium text-gray-400">No messages yet</h3>
                <p className="mt-1 text-sm text-gray-500">Start a conversation with {selectedModel.name}</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-3xl rounded-lg px-4 py-2 ${
                      message.role === 'user'
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-800 text-white border border-gray-700'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        {message.role === 'user' ? (
                          <UserIcon className="h-6 w-6" />
                        ) : (
                          <SparklesIcon className="h-6 w-6" />
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                        <div className="mt-1 text-xs opacity-70">
                          {(message.timestamp instanceof Date ? message.timestamp : new Date(message.timestamp)).toLocaleTimeString()}
                          {message.model && ` • ${message.model}`}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="flex items-end space-x-4 p-4 bg-gray-800 rounded-lg border border-gray-700">
            <div className="flex-1">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                rows={1}
                style={{ minHeight: '44px', maxHeight: '120px' }}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white p-3 rounded-lg transition-colors"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <PaperAirplaneIcon className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;