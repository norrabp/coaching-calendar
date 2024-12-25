import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from '@components/Layout';
import Users from '@core/users/pages/Users';
import Login from '@core/auth/pages/Login';
import Register from '@core/auth/pages/Register';
import StudentHome from '@core/appointments/StudentHome';
import CoachHome from '@core/appointments/CoachHome';
import { UserProvider } from '@context/UserContext';

const App: React.FC = () => {
  return (
    <Router>
      <UserProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Users />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/student" element={<StudentHome />} />
            <Route path="/coach" element={<CoachHome />} />
            </Routes>
          </Layout>
      </UserProvider>
    </Router>
  );
};

export default App;
