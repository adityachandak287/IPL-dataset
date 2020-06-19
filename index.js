const express = require("express");
const app = express();
const bodyParser = require("body-parser");

var mongo = require("mongodb").MongoClient;
const mongoURI = "mongodb://localhost:27017";
const PORT = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs");

mongo.connect(
  mongoURI,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true
  },
  (err, client) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log("Connected to MongoDB");
    const db = client.db("ipl");
    const matchesCollection = db.collection("tables");

    app.get("/", (req, res) => {
      matchesCollection.find().toArray(function(err, tables) {
        if (err) console.log(err);
        // else console.log(docs);

        res.render("index", {
          tables: tables
        });
      });
    });

    app.get("/table/:season", (req, res) => {
      matchesCollection
        .find({ season: req.params.season })
        .toArray(function(err, table) {
          if (err) console.log(err);
          // else console.log(docs);

          res.render("table", {
            season: table[0]
          });
        });
    });

    app.get("/team/:teamname", (req, res) => {
      db.collection("matches")
        .find({
          $or: [{ team1: req.params.teamname }, { team2: req.params.teamname }]
        })
        .toArray(function(err, matches) {
          if (err) console.log(err);

          var teamWise = {};

          matches.forEach(match => {
            var currSeason = "" + match["season"];
            if (!Object.keys(teamWise).includes(currSeason)) {
              teamWise[currSeason] = [];
            }
            teamWise[currSeason].push(match);
          });
          // res.send(teamWise);
          res.render("team", {
            seasons: teamWise
          });
        });
    });

    app.listen(PORT, function() {
      console.log(`Listening on port ${PORT}`);
    });
  }
);
