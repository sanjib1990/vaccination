"use strict";

require('dotenv').config();

let plan    = require("flightplan");
let args    = require('minimist')(process.argv.slice(2));
let getCodeFolder = () => {
    return "/home/ubuntu/vaccination";
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
        remote.log("!! STARTING UPDATE !!");

        remote.log("Fetching all the branches.");
        remote.exec("git fetch --all --prune");

        remote.log("Checkout branch " + envs.branch);
        remote.exec("git checkout " + envs.branch);

        remote.log("Pull from git repository.");
        remote.exec("git pull origin "+ envs.branch);

        remote.log("Instaling dependencies");
        remote.exec("/home/ubuntu/.local/bin/pip install -r requirements.txt");

        remote.log("!! UPDATE DONE !!");
    });
});

plan.local(local => {
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