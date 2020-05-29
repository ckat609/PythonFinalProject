content = document.getElementById('js_navmenu').innerHTML

mySession = '<%= Session["logged_in"] %>';

console.log(mySession)
if (true) {
    document.getElementById('js_navmenu').innerHTML = `
        <nav class='navbar navbar-expand-lg navbar-dark bg-dark'>
            <a class='navbar-brand' href='/'><span class="navbar-brand mb-0 h1 btn btn-warning text-dark"><h5>myMDB</h5></span></a>
            <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarSupportedContent' aria-controls='navbarSupportedContent' aria-expanded='false'
                aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
            </button>
    
            <div class='collapse navbar-collapse' id='navbarSupportedContent'>
                <ul class='navbar-nav'>
                    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Movies & Shows
                        </a>
                        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                        <a class='dropdown-item' href='/shows/add'>Add new</a>
                        <a class='dropdown-item' href='/shows/list'>List all</span></a>
                        </div>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle' dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Genres
                        </a>
                        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                        <a class='dropdown-item' href='/shows/genre/add'>Add new</a>
                        <a class='dropdown-item' href='/shows/genre/list'>List all</a>
                        </div>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Networks
                        </a>
                        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                        <a class='dropdown-item' href='/shows/network/add'>Add new</a>
                        <a class='dropdown-item' href='/shows/network/list'>List all</a>
                        </div>
                    </li>
                </ul>
            </div>
        ` + content + `</nav>`;
} else {
    document.getElementById('js_navmenu').innerHTML = `
    <nav class='navbar navbar-expand-lg navbar-dark bg-dark'>
        <a class='navbar-brand' href='/'><span class="navbar-brand mb-0 h1 btn btn-warning text-dark">myMDB</span></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarSupportedContent' aria-controls='navbarSupportedContent' aria-expanded='false'
            aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>
    </nav>
        `
}