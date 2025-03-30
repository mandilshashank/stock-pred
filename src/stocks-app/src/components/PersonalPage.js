import React from 'react';

function PersonalPage() {
    const user = JSON.parse(localStorage.getItem('user'));

    return (
        <div>
            <h1>Welcome, {user.name}</h1>
            <img src={user.picture} alt="Profile" />
            <p>Email: {user.email}</p>
        </div>
    );
}

export default PersonalPage;