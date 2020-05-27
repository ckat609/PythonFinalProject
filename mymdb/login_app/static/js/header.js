content = document.getElementById('js_navmenu').innerHTML

document.getElementById('js_navmenu').innerHTML = `
    <nav class='navbar navbar-expand-lg navbar-dark bg-dark'>
        <a class='navbar-brand' href='/user/login/success'><span class="navbar-brand mb-0 h1 btn btn-warning text-dark">myMDB</span></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarSupportedContent' aria-controls='navbarSupportedContent' aria-expanded='false'
            aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>

        <div class='collapse navbar-collapse' id='navbarSupportedContent'>
            <ul class='navbar-nav'>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/add'>Add Title</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/list'>Movie/Shows List<span class='sr-only'>(current)</span></a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/network/add'>Add Network</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/network/list'>Network list</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/genre/add'>Add Genre</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/shows/genre/list'>Genre list</a>
                </li>
            </ul>
        </div>
    ` + content + `</nav>`;