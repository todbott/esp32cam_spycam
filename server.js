import GetPictures from './getPictures.js';

import express from 'express';
const app = express();

app.set('view engine', 'ejs');

app.get('/', async (req, res) => {
    let pics = await GetPictures()
    let jdata = JSON.stringify(pics)
    let p = ""
    Object.entries(pics.data).forEach(([key, val]) => {
        p = `<img src="data:image/jpeg;base64, ${val}" id="feed">`
    });
    res.render('pages/page', {image: p})
    
});

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});
