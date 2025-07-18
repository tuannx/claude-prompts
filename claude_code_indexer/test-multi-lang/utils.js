// JavaScript utility functions

class DataProcessor {
    constructor() {
        this.data = [];
    }
    
    process(input) {
        return input.map(x => x * 2);
    }
}

function formatData(data) {
    return JSON.stringify(data, null, 2);
}

module.exports = { DataProcessor, formatData };