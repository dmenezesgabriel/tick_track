import React from 'react';

function Sidebar() {
    let toggleClass = () => {
        const sidebarCollapse = document.querySelector('#sidebarCollapse');
        const sidebar = document.querySelector('#sidebar');
        const content = document.querySelector('#content');

        sidebar.classList.toggle('active');
        content.classList.toggle('active');
        sidebarCollapse.classList.toggle('active');
      };
    return (
        <nav class="col-md-2 d-md-block sidebar bg-dark" id="sidebar">

            <button id="dismiss" onClick={toggleClass} class="btn close" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            <div class="sidebar-header text-center bg-dark">
                <h1>Tick Track</h1>
            </div>
            <hr></hr>
            <div class="profile-section components">
                <ul class="list-unstyled components text-left">
                    <li>
                        <a href="/"><i className="fas fa-chart-line"></i> Dashboard</a>
                    </li>
                    <li>
                        <a href="/"><i className="fal fa-clock"></i> Pomodoro Timer</a>
                    </li>
                    <li>
                        <a href="/"><i className="fal fa-border-all"></i> Board</a>
                    </li>
                    <li>
                        <a href="/"><i className="far fa-bookmark"></i> Notes</a>
                    </li>
                    <hr></hr>
                </ul>
            </div>
        </nav>
    )
}

export default Sidebar;