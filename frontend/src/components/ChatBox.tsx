import React, { useState } from 'react';
import axios from 'axios';
import { Send, User, Bot, Loader2, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', sender: 'bot', text: 'Hello! I am Divya, your intelligent Get Smth AI assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://localhost:5000/api/chat', {
        message: input,
        userId: 'demo-user-123',
        history: messages.map(m => ({ role: m.sender === 'user' ? 'user' : 'assistant', content: m.text }))
      });
      
      const botMsg: Message = { id: Date.now().toString(), sender: 'bot', text: res.data.reply || 'Sorry, I could not understand that.' };
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { id: Date.now().toString(), sender: 'bot', text: 'Error connecting to the server. Please try again later.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full h-full bg-white dark:bg-gray-800 rounded-[2rem] shadow-lg border border-gray-100 dark:border-gray-700/50 overflow-hidden transition-all duration-300 relative">
      <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md p-5 text-gray-800 dark:text-white flex items-center justify-between border-b border-gray-100 dark:border-gray-700/50 z-20 sticky top-0">
        <div className="flex items-center">
          <div className="bg-emerald-50 dark:bg-emerald-900/30 p-2.5 rounded-2xl mr-4 flex-shrink-0 animate-pulse-slow">
             <Bot size={24} className="text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <h3 className="font-extrabold text-lg tracking-tight">Divya Support</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center font-medium mt-0.5"><Sparkles size={10} className="mr-1 text-emerald-500" /> AI Assistant</p>
          </div>
        </div>
      </div>
      
      <div className="flex-1 p-6 overflow-y-auto flex flex-col space-y-6 scroll-smooth z-10 bg-gray-50/50 dark:bg-gray-900/20 relative">
        {messages.map((msg, index) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in-up`} style={{ animationFillMode: 'both', animationDelay: `${(index > messages.length - 2) ? 0 : 0}ms` }}>
            <div className={`flex items-end max-w-[85%] ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.sender === 'user' ? 'bg-emerald-600 ml-2 shadow-md shadow-emerald-500/20' : 'bg-white dark:bg-gray-700 mr-2 shadow-sm border border-gray-100 dark:border-gray-600'}`}>
                {msg.sender === 'user' ? <User size={16} className="text-white" /> : <Bot size={16} className="text-emerald-600 dark:text-emerald-400" />}
              </div>
              <div className={`p-4 rounded-3xl text-sm leading-relaxed ${msg.sender === 'user' ? 'bg-emerald-600 text-white rounded-br-sm shadow-md shadow-emerald-500/10' : 'bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-gray-800 dark:text-gray-200 shadow-sm rounded-bl-sm'}`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start animate-fade-in-up">
            <div className="flex items-end max-w-[85%]">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white dark:bg-gray-700 mr-2 flex items-center justify-center shadow-sm border border-gray-100 dark:border-gray-600">
                <Bot size={16} className="text-emerald-600 dark:text-emerald-400" />
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-3xl rounded-bl-sm border border-gray-100 dark:border-gray-700 shadow-sm flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-emerald-500/60 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-emerald-500/60 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-emerald-500/60 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 z-20">
        <div className="flex items-center bg-gray-50 dark:bg-gray-900/50 rounded-full border border-gray-200 dark:border-gray-700 shadow-inner focus-within:ring-2 focus-within:ring-emerald-500/50 focus-within:border-emerald-500 transition-all duration-300 pl-5 pr-2 py-2">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
            className="flex-1 bg-transparent border-none outline-none text-gray-800 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500 text-sm"
          />
          <button 
             onClick={sendMessage}
             className={`ml-2 p-2.5 rounded-full transition-all duration-300 flex items-center justify-center ${input.trim() ? 'bg-emerald-600 text-white shadow-md hover:shadow-lg hover:-translate-y-0.5' : 'bg-white dark:bg-gray-800 text-gray-400 dark:text-gray-500 shadow-sm border border-gray-100 dark:border-gray-700'}`}
             disabled={loading || !input.trim()}
          >
            <Send size={16} className={input.trim() ? 'translate-x-[1px] translate-y-[-1px]' : ''} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
