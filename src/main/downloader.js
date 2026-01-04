const axios = require('axios');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const { app } = require('electron');

async function downloadPodcast(url) {
  try {
    const response = await axios.get(url, { responseType: 'stream' });
    const ext = url.split('.').pop().split('?')[0];
    const filename = path.join(app.getPath('temp'), `${uuidv4()}.${ext}`);
    const writer = fs.createWriteStream(filename);
    
    response.data.pipe(writer);
    
    return new Promise((resolve, reject) => {
      writer.on('finish', () => resolve(filename));
      writer.on('error', reject);
    });
  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
}

module.exports = { downloadPodcast };