import firebase from 'firebase/app'
import 'firebase/auth'

// The configuration below is not sensitive data. You can serenely add your config here
const config = {
  apiKey: 'AIzaSyBZayTfWkaB3q32wn15YEYvL1hsideBX64',
  authDomain: 'zanah-news-updates.firebaseapp.com',
  databaseURL: 'https://zanah-news-updates.firebaseio.com',
  projectId: 'zanah-news-updates',
  storageBucket: 'zanah-news-updates.appspot.com',
  messagingSenderId: '683935734855',
  appId: '1:683935734855:web:9a3c9be7c5ed52a641a562',
  measurementId: 'G-3YWVRFGR8C'
}

firebase.initializeApp(config)
