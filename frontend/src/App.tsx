import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import ChatBox from './components/ChatBox';
import { PackageSearch, ShoppingBag, Truck, LogIn, Sun, Moon, LogOut, ArrowRight, UserPlus, AlertCircle } from 'lucide-react';

const Navbar = ({ theme, toggleTheme, user, setUser }: any) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    setUser(null);
    navigate('/');
  };

  return (
    <nav className="w-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-md shadow-sm border-b border-gray-100 dark:border-gray-800 p-4 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center text-emerald-600 dark:text-emerald-400 font-extrabold text-2xl tracking-tight hover:scale-105 transition-transform duration-300">
          <ShoppingBag className="mr-2" />
          Get Smth
        </Link>
        <div className="flex items-center space-x-6 text-gray-600 dark:text-gray-300 font-medium select-none">
          <Link to="/" className={`hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors duration-200 ${location.pathname === '/' ? 'text-emerald-600 dark:text-emerald-400 font-semibold' : ''}`}>Shop</Link>
          <Link to="/orders" className={`hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors duration-200 ${location.pathname === '/orders' ? 'text-emerald-600 dark:text-emerald-400 font-semibold' : ''}`}>Orders</Link>
          <button onClick={toggleTheme} className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/50">
            {theme === 'dark' ? <Sun size={20} className="text-yellow-400" /> : <Moon size={20} className="text-gray-600" />}
          </button>
          
          {user ? (
            <button onClick={handleLogout} className="flex items-center space-x-2 bg-rose-50 text-rose-600 dark:bg-rose-500/10 dark:text-rose-400 px-4 py-2 rounded-full hover:bg-rose-100 dark:hover:bg-rose-500/20 transition-all duration-300 font-medium">
              <LogOut size={18} />
              <span>Logout</span>
            </button>
          ) : (
            <Link to="/login" className="flex items-center space-x-2 bg-emerald-600 text-white px-5 py-2 rounded-full hover:bg-emerald-700 hover:shadow-lg hover:shadow-emerald-500/30 transition-all duration-300 transform hover:-translate-y-0.5">
              <LogIn size={18} />
              <span>Sign In</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

const Home = () => (
  <div className="w-full h-full flex mt-6 gap-8 relative z-10 transition-all duration-500 animate-fade-in-up">
    {/* Left Side: Store */}
    <div className="flex-1 flex flex-col gap-8 px-4">
      <div className="w-full text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-6 text-gray-900 dark:text-white tracking-tight">
          Experience <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400">Brilliance</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed">
          Explore our curated collection of extraordinary products. Have questions? Ask Divya, our intelligent AI assistant!
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left pb-10">
        {[
          { name: 'Smart Watch X', price: '₹199.99', from: 'from-emerald-400', to: 'to-cyan-400', delay: '0' },
          { name: 'Aero Pods Pro', price: '₹129.99', from: 'from-purple-400', to: 'to-indigo-400', delay: '100' },
          { name: 'ErgoMech Keyboard', price: '₹159.00', from: 'from-orange-400', to: 'to-rose-400', delay: '200' },
          { name: 'Lens 4K Drone', price: '₹499.99', from: 'from-blue-400', to: 'to-sky-400', delay: '300' },
        ].map((item, i) => (
          <div key={i} className={`p-1 rounded-3xl bg-gradient-to-br ${item.from} ${item.to} hover:shadow-xl hover:shadow-emerald-500/20 transition-all duration-500 hover:-translate-y-1`} style={{ animationDelay: `${item.delay}ms` }}>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-[22px] h-full flex flex-col justify-between backdrop-blur-3xl bg-white/90 dark:bg-gray-800/90">
              <div>
                 <div className={`w-full h-32 rounded-xl mb-4 bg-gradient-to-r ${item.from} ${item.to} opacity-20`} />
                 <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-2">{item.name}</h3>
              </div>
              <div className="flex justify-between items-center mt-4">
                <p className="text-2xl font-black text-gray-900 dark:text-gray-100">{item.price}</p>
                <button className="bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-4 py-2 rounded-full font-medium text-sm hover:scale-105 transition-transform">Buy Now</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>

    {/* Right Side: Chat Panel */}
    <div className="hidden lg:block w-[420px] h-[calc(100vh-140px)] flex-shrink-0 animate-fade-in-up sticky top-24 z-20 pb-10">
      <ChatBox />
    </div>
  </div>
);

const Orders = () => (
  <div className="w-full flex mt-6 gap-8 relative z-10 transition-all duration-500 animate-fade-in-up">
    {/* Left Side: Orders */}
    <div className="flex-1 flex flex-col px-4 pb-10">
      <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl p-8 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700/50">
        <h2 className="text-3xl font-extrabold mb-8 flex items-center text-gray-900 dark:text-white tracking-tight">
          <Truck className="mr-3 text-emerald-500 w-8 h-8" /> Order History
        </h2>
        
        <div className="space-y-4">
          {[
            { id: 'GS-883921', date: 'May 15, 2026', total: '₹149.99', status: 'Shipped', statusColor: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-400' },
            { id: 'GS-592100', date: 'May 10, 2026', total: '₹34.50', status: 'Delivered', statusColor: 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400' },
            { id: 'GS-110293', date: 'May 02, 2026', total: '₹89.00', status: 'Refunded', statusColor: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300' }
          ].map((order, i) => (
            <div key={order.id} className="p-6 border border-gray-100 dark:border-gray-700/50 rounded-2xl bg-white dark:bg-gray-800 hover:shadow-lg transition-shadow duration-300 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 group">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform duration-300">
                  <PackageSearch size={24} />
                </div>
                <div>
                  <p className="font-bold text-gray-900 dark:text-white text-lg group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">Order #{order.id}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Placed on {order.date}</p>
                </div>
              </div>
              <div className="flex items-center gap-6 justify-between sm:justify-end">
                <p className="font-bold text-gray-900 dark:text-white text-xl">{order.total}</p>
                <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-wide ${order.statusColor}`}>
                  {order.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>

    {/* Right Side: Chat Panel */}
    <div className="hidden lg:block w-[420px] h-[calc(100vh-140px)] flex-shrink-0 animate-fade-in-up sticky top-24 z-20 pb-10">
      <ChatBox />
    </div>
  </div>
);

const Auth = ({ setUser }: { setUser: (u: any) => void }) => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email.includes('@')) {
      setError('Please enter a valid email address.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    if (!isLogin && name.trim().length < 2) {
      setError('Please enter your full name.');
      return;
    }

    setUser({ email, name: isLogin ? 'Demo User' : name });
    navigate('/');
  };

  return (
    <div className="w-full flex-1 flex justify-center items-center animate-fade-in-up py-10 px-4 min-h-[calc(100vh-100px)] relative z-10 transition-all duration-500">
      <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl p-10 rounded-3xl shadow-2xl w-full max-w-md border border-gray-100 dark:border-gray-700/50 relative overflow-hidden transition-all duration-300">
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-400 to-teal-500" />
        
        <div className="flex justify-center mb-8">
          <div className="bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 p-5 rounded-full shadow-inner">
            {isLogin ? <LogIn size={32} /> : <UserPlus size={32} />}
          </div>
        </div>
        
        <h2 className="text-3xl font-extrabold text-center text-gray-900 dark:text-white mb-2 tracking-tight">
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </h2>
        <p className="text-center text-gray-500 dark:text-gray-400 mb-6">
          {isLogin ? 'Sign in to access your Get Smth account' : 'Join us to get personalized recommendations'}
        </p>

        {error && (
          <div className="mb-6 p-4 bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/20 rounded-xl flex items-center text-rose-600 dark:text-rose-400 text-sm font-medium animate-fade-in-up">
            <AlertCircle size={18} className="mr-2 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div className="animate-fade-in-up" style={{ animationDuration: '0.3s' }}>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5 ml-1">Full Name</label>
              <input 
                type="text" 
                value={name}
                onChange={e => setName(e.target.value)}
                className="w-full px-5 py-3 bg-gray-50 dark:bg-gray-900/50 border border-transparent dark:border-gray-700 rounded-xl focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-gray-900 dark:text-white transition-all outline-none"
                placeholder="John Doe"
              />
            </div>
          )}
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5 ml-1">Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full px-5 py-3 bg-gray-50 dark:bg-gray-900/50 border border-transparent dark:border-gray-700 rounded-xl focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-gray-900 dark:text-white transition-all outline-none"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5 ml-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full px-5 py-3 bg-gray-50 dark:bg-gray-900/50 border border-transparent dark:border-gray-700 rounded-xl focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-gray-900 dark:text-white transition-all outline-none"
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 px-4 rounded-xl shadow-lg shadow-emerald-500/30 transition-all duration-300 transform hover:-translate-y-1 mt-6 flex justify-center items-center group">
            <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
            <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
          </button>
        </form>
        
        <div className="mt-8 text-center">
          <button 
            type="button" 
            onClick={() => { setIsLogin(!isLogin); setError(''); }}
            className="text-emerald-600 dark:text-emerald-400 font-semibold hover:underline transition-colors"
          >
            {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState<{ email: string; name: string } | null>(null);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  return (
    <Router>
      <div className={`min-h-screen flex flex-col transition-colors duration-500 font-sans overflow-x-hidden ${theme === 'dark' ? 'dark bg-[#0f172a]' : 'bg-[#f8fafc]'}`}>
        <Navbar theme={theme} toggleTheme={toggleTheme} user={user} setUser={setUser} />

        <main className="flex-1 w-full max-w-7xl mx-auto flex w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/login" element={<Auth setUser={setUser} />} />
          </Routes>
        </main>
        
        {/* Background decorative elements */}
        <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none -z-10">
          <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-emerald-400/10 dark:bg-emerald-900/20 blur-[120px]" />
          <div className="absolute top-[40%] -right-[10%] w-[40%] h-[60%] rounded-full bg-teal-400/10 dark:bg-teal-900/20 blur-[120px]" />
        </div>
      </div>
    </Router>
  );
}

export default App;
