import fetch from "node-fetch";

async function GetPictures() {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      };
  
      try {
        const response = await fetch('https://us-central1-hotaru-kanri.cloudfunctions.net/room-stats', requestOptions)
        const json = await response.json();
        return json
      } catch (e) {
        console.log(e)
        return "no pictures"
      }
}

export default GetPictures;