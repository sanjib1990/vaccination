"use strict";

require('dotenv').config();

let plan    = require("flightplan");
let args    = require('minimist')(process.argv.slice(2));
let getCodeFolder = () => {
    return "/var/www/html/web";
};

let envs    = {
    host: getHost(),
    privateKey: getPEMFileLocation(),
    branch: getBranch()
};

plan.target('deploy', {
    host: envs.host,
    username: process.env.AWS_USER_NAME,
    agent: process.env.SSH_AUTH_SOCK,
    branch: envs.branch,
    privateKey: envs.privateKey
});

//Deploy Plan
plan.remote(remote => {
    remote.with('cd ' + getCodeFolder(), () => {
        remote.log("Server maintanence mode on");
        remote.exec("php artisan down");

        remote.log("Fetching all the branches.");
        remote.exec("git fetch --all --prune");

        remote.log("Checkout branch " + envs.branch);
        remote.exec("git checkout " + envs.branch);

        remote.log("Pull from git repository.");
        remote.exec("git pull origin "+ envs.branch);

        remote.log("Instaling composer dependencies");
        remote.exec("composer install");

        remote.log("Instaling Node dependencies");
        remote.exec("~/.nvm/versions/node/v6.11.2/bin/node ~/.nvm/versions/node/v6.11.2/bin/npm install");

        remote.log("Combine assets");
        remote.exec("~/.nvm/versions/node/v6.11.2/bin/node ~/.nvm/versions/node/v6.11.2/bin/npm run dev");

        remote.log("Running migration");
        remote.exec("php artisan migrate");

        remote.log("Update Asset Version");
        remote.exec("php artisan update:cache");

        remote.log("Permission for shared folders");
        remote.exec("sudo chmod -R 777 bootstrap");
        remote.exec("sudo chmod -R 777 storage");
        remote.exec("sudo chmod -R 777 public");

        remote.log("Server maintanence mode off");
        remote.exec("php artisan up");
    });
});

plan.local(local => {
   let Slack    = require("slack-node");
   let slack    = new Slack(process.env.SLACK_API_TOKEN);

    slack.api('chat.postMessage', {
        username: "UBU-Deployer",
        icon_emoji: ":space_invader:",
        text:'Deploy Successfull on `'+ envs.host +'` Branch: `'+ envs.branch + '` Codebase: `website`',
        channel:'#deploy'
    }, function(err, response){
    });
});

function getUserHome() {
    return process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];
}

function getPEMFileLocation() {
    let file = args.env === 'prod' ? process.env.AWS_PROD_PEM_FILE : process.env.AWS_PEM_FILE;

    return getUserHome() + file;
}

function getHost() {
    return args.env === 'prod' ? process.env.AWS_PROD_HOST : process.env.AWS_STAGING_HOST;
}

function getBranch() {
    if (args.branch === undefined || args.branch === "") {
        args.branch = 'master';
    }

    return args.branch;
}