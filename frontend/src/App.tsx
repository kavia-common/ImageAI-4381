import React from 'react';
import { Link, NavLink, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import ImageClassification from './pages/ImageClassification';
import ObjectDetection from './pages/ObjectDetection';
import VideoDetection from './pages/VideoDetection';

const navStyle: React.CSSProperties = {
  display: 'flex',
  gap: '16px',
  padding: '12px 16px',
  borderBottom: '1px solid #eee',
  alignItems: 'center'
};

const activeStyle: React.CSSProperties = {
  fontWeight: 'bold',
  color: '#0d6efd'
};

export default function App() {
  return (
    <div>
      <header style={navStyle}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit', fontWeight: 700 }}>
          ImageAI
        </Link>
        <nav style={{ display: 'flex', gap: 12 }}>
          <NavLink to="/" end style={({ isActive }) => (isActive ? activeStyle : undefined)}>
            Home
          </NavLink>
          <NavLink to="/classification" style={({ isActive }) => (isActive ? activeStyle : undefined)}>
            Image Classification
          </NavLink>
          <NavLink to="/detection" style={({ isActive }) => (isActive ? activeStyle : undefined)}>
            Object Detection
          </NavLink>
          <NavLink to="/video" style={({ isActive }) => (isActive ? activeStyle : undefined)}>
            Video Detection
          </NavLink>
        </nav>
      </header>
      <main style={{ padding: 16, maxWidth: 960, margin: '0 auto' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/classification" element={<ImageClassification />} />
          <Route path="/detection" element={<ObjectDetection />} />
          <Route path="/video" element={<VideoDetection />} />
        </Routes>
      </main>
      <footer style={{ padding: 16, textAlign: 'center', color: '#666' }}>
        © {new Date().getFullYear()} ImageAI Demo
      </footer>
    </div>
  );
}
