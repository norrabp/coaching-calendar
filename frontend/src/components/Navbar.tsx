import { useUser } from '@context/UserContext';
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');
  const { user } = useUser();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">Coach App</Link>
        
        <div className="navbar-nav ms-auto">
          {isAuthenticated ? (
            <div className="d-flex align-items-center">
              <button className="btn btn-outline-light me-3" onClick={handleLogout}>
                Logout
              </button>
            </div>
          ) : (
            <Link className="btn btn-outline-light" to="/login">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
