import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import ProductList from './ProductList';
import ProductDetail from './ProductDetail';
import Cart from './Cart';
import Login from './Login';
import Signup from './Signup';
import Logout from './Logout';
import Checkout from './Checkout';

function App() {
  const [user, setUser] = useState();

  useEffect(() => {
    fetch("/api/check_session", {
      method: 'GET',
      credentials: 'include',
    })
      .then((r) => {
        if (r.ok) {
          r.json().then((userData) => {
            setUser(userData);
          });
        } else {
          setUser(null);
        }
      });
  }, []);


  return (
    <Router>
      <div className="App">
        <Header />
        <Switch>
          <Route path="/" exact component={ProductList} />
          <Route path="/product/:id" component={ProductDetail} />
          <Route path="/cart" component={Cart} />
          <Route path="/login" element={<Login user={user} setUser={setUser} />} />
          <Route path="/signup" element={<Signup user={user} setUser={setUser} />} />
          <Route path="/logout" element={<Logout setUser={setUser} />} />
          <Route path="/checkout" component={Checkout} />
        </Switch>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
