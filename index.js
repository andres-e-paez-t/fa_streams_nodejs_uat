const Listener = require('dj-dna-streaming-javascript').Listener;
const sqlite3 = require('sqlite3');

const db = new sqlite3.Database('test_listener_nodejs.sqlite3');

db.serialize(() => {
    db.run('CREATE TABLE IF NOT EXISTS received_articles (an TEXT, ingestion_datetime TEXT)');
});

const listener = new Listener();

async function writeOnMessage(message) {
    return new Promise((resolve, reject) =>  {
        const data = JSON.parse(message.data).data[0];
        const id = data.id;
        const ingestion_datetime = data.attributes.ingestion_datetime;
        
        function dbCallback(err) {
            if (err) {
                reject(err);
            } else {
                console.info(`Written: ${id}`);
                resolve();
            }
        };
        
        db.run('INSERT INTO received_articles (an, ingestion_datetime) VALUES (?, ?)', [id, ingestion_datetime], dbCallback);
    });
};

listener.listen(writeOnMessage);

function closeClient() {
    console.log('Killed!');
    console.log('Closing listener');
    listener.closeListener();
    console.log('Closing DB');
    db.close(function callback(err) {
        if (err){
            console.error(`Error encountered while closing DB: ${err}`);
        } else {
            console.info('DB correctly closed!');
        }
    });
}

process.on('SIGINT', closeClient);
process.on('SIGTERM', closeClient);


setTimeout(() => {listener.closeListener();}, 1000 * 60 * 60 * 2);

setTimeout(() => {listener.listen(writeOnMessage);}, 1000 * 60 * 60 * 2.5);

setTimeout(closeClient, 1000 * 60 * 60 * 5);
