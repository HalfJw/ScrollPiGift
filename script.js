fetch('http://10.0.0.232:5000/')
  .then(response => response.json())
  .then(data => console.log(data));