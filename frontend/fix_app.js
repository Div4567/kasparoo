const fs = require('fs');
const p = '/home/anjishnu-nandi/Documents/GitHub/get_smth/frontend/src/App.tsx';

let code = `import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatBox from './components/ChatBox';
import { PackageSearch, ShoppingBag, Truck, Loader2 } from 'lucide-react';

interface Order {
  _id: string;
  orderId: string;
  userId: string;
  status: string;
  createdAt: string;
}

interface Product {
  _id: string;
  name: string;
  price: number;
  imageUrl?: string;
}

function App() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loadingOrders, setLoadingOrders] = useState<boolean>(true);
  const [errorOrders, setErrorOrders] = useState<string | null>(null);

  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loadingRecs, setLoadingRecs] = useState<boolean>(true);
  const [errorRecs, setErrorRecs] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/orders/user123');
        setOrders(response.data);
      } catch (err) {
        setErrorOrders("Failed to load orders. Please try again later.");
      } finally {
        setLoadingOrders(false);
      }
    };

    const fetchRecommendations = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/products');
        setRecommendations(response.data.slice(0, 2)); // Show mock 2 products
      } catch (err) {
        setErrorRecs("Failed to load recommendations.");
      } finally {
        setLoadingRecs(false);
      }
    };

    fetchOrders();
    fetchRecommendations();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      <nav className="w-full bg-white shadow-sm p-4 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center text-blue-600 font-extrabold text-2xl tracking-tight">
            <ShoppingBag className="mr-2" />
            Get Smth
          </div>
          <div className="flex space-x-6 text-gray-600 font-medium">
            <a href="/" className="hover:text-blue-600 transition">Shop</a>
            <a href="/" className="hover:text-blue-600 transition">Orders</a>
            <a href="/" className="hover:text-blue-600 transition">Support</a>
          </div>
        </div>
      </nav>

      <main className="flex-1 w-full max-w-6xl mx-auto p-4 flex flex-col md:flex-row gap-6 mt-6">
        <div className="flex-1 flex flex-col gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-xl font-bold mb-4 flex items-center"><Truck className="mr-2 text-blue-500" /> Recent Orders</h2>
            
            {loadingOrders ? (
              <div className="flex flex-col items-center justify-center p-8 text-gray-500">
                <Loader2 className="animate-spin mb-2" size={32} />
                <p>Loading your orders...</p>
              </div>
            ) : errorOrders ? (
              <div className="p-4 border border-red-200 bg-red-50 text-red-600 rounded">
                {errorOrders}
              </div>
            ) : orders.length === 0 ? (
              <div className="p-8 text-center text-gray-500 border border-dashed rounded bg-gray-50">
                <PackageSearch className="mx-auto mb-2 text-gray-400" size={48} />
                <p>You haven\\'t placed any orders yet.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {orders.map((order) => (
                  <div key={order._id} className="p-4 border rounded bg-gray-50 flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-gray-800">Order #{order.orderId}</p>
                      <p className="text-sm text-gray-500">Placed on {new Date(order.createdAt).toLocaleDateString()}</p>
                    </div>
                    <span className={\`px-3 py-1 rounded-full text-sm font-semibold \${
                      order.status === 'Delivered' ? 'bg-green-100 text-green-700' :
                      order.status === 'Shipped' ? 'bg-blue-100 text-blue-700' :
                      'bg-orange-100 text-orange-700'
                    }\`}>
                      {order.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-xl font-bold mb-4 flex items-center"><PackageSearch className="mr-2 text-purple-500" /> Recommended for You</h2>
            
            {loadingRecs ? (
              <div className="flex flex-col items-center justify-center p-8 text-gray-500">
                <Loader2 className="animate-spin mb-2" size={32} />
                <p>Loading recommendations...</p>
              </div>
            ) : errorRecs ? (
              <div className="p-4 border border-red-200 bg-red-50 text-red-600 rounded">
                {errorRecs}
              </div>
            ) : recommendations.length === 0 ? (
              <div className="p-8 text-center text-gray-500 border border-dashed rounded bg-gray-50">
                <PackageSearch className="mx-auto mb-2 text-gray-400" size={48} />
                <p>No recommendations available.</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4 text-center">
                {recommendations.map(product => (
                  <div key={product._id} className="border p-4 rounded-lg bg-gray-50 hover:shadow-md transition cursor-pointer flex flex-col items-center justify-between">
                    <div className="w-full h-32 bg-gray-200 mb-2 rounded mx-auto overflow-hidden bg-gradient-to-tr from-gray-200 to-gray-300 flex items-center justify-center">
                      <ShoppingBag className="text-gray-400" size={32}/>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-700 mt-2">{product.name}</p>
                      <p className="text-blue-600 font-bold">${product.price}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="w-full md:w-[400px] h-[600px] flex-shrink-0 border bg-white rounded-xl relative shadow-lg">
          <div className="absolute inset-0">
             <ChatBox />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
`;
fs.writeFileSync(p, code);
