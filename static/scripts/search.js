const movieNames = document.querySelectorAll('.movie-name');

movieNames.forEach((movieName) => {
  movieName.addEventListener('mouseover', () => {
    const imdbId = movieName.dataset.imdbId;
    fetch(`https://www.omdbapi.com/?i=${imdbId}&apikey=your_api_key`)
      .then((response) => response.json())
      .then((data) => {
        const moviePreview = document.getElementById('movie-preview');
        moviePreview.innerHTML = `
          <iframe src="https://www.imdb.com/title/${data.imdbID}/" frameborder="0" width="100%" height="100%"></iframe>
        `;
        moviePreview.style.display = 'block';
      })
      .catch((error) => console.error(error));
  });

  movieName.addEventListener('mouseout', () => {
    const moviePreview = document.getElementById('movie-preview');
    moviePreview.style.display = 'none';
  });
});
