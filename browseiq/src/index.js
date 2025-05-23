import React from 'react';
import ReactDOM from 'react-dom/client';
import PropTypes from 'prop-types';
import './index.css'; // Create this for styling

// FloatingButton Component
function FloatingButton({ icon, onClick }) {
  return (
    <div className="floating-btn" onClick={onClick}>
      {icon}
    </div>
  );
}

FloatingButton.propTypes = {
  icon: PropTypes.node,
  onClick: PropTypes.func,
};

FloatingButton.defaultProps = {
  icon: '✍️',
  onClick: () => alert('Floating button clicked!'),
};

// Add button to DOM
const rootDiv = document.createElement('div');
rootDiv.id = 'my-react-root';
document.body.appendChild(rootDiv);

// Render component
const root = ReactDOM.createRoot(document.getElementById('my-react-root'));
root.render(<FloatingButton />);
