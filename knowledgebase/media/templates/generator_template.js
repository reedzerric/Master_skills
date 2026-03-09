/**
 * P5.JS GENERATIVE ART - BEST PRACTICES
 */

let params = {
    seed: 12345,
    colorPalette: ['#d97757', '#6a9bcc', '#788c5d', '#b0aea5'],
};

function initializeSeed(seed) {
    randomSeed(seed);
    noiseSeed(seed);
}

function setup() {
    createCanvas(800, 800);
    initializeSeed(params.seed);
}

function draw() {
    // Implement your algorithm here
}

class Entity {
    constructor() {
        // Initialize entity properties
    }
    update() {}
    display() {}
}

function updateParameter(paramName, value) {
    params[paramName] = value;
}

function regenerate() {
    initializeSeed(params.seed);
}
