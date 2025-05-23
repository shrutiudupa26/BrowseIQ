import React from 'react';
import ReactDOM from 'react-dom/client';
import PropTypes from 'prop-types';
import './index.css';

function FloatingButton({ icon, onClick }) {
  return (
    <button className="floating-btn" onClick={onClick}>
      {icon}
    </button>
  );
}

FloatingButton.propTypes = {
  icon: PropTypes.node,
  onClick: PropTypes.func,
};

FloatingButton.defaultProps = {
  icon: '✍️',
  onClick: () => alert('You clicked the floating button!'),
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<FloatingButton />);
