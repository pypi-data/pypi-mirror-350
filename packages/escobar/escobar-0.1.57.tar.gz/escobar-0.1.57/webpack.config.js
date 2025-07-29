const path = require('path');

module.exports = {
    // Configure webpack to completely disable source maps for problematic packages
    module: {
        rules: [
            {
                test: /\.js$/,
                enforce: 'pre',
                use: ['source-map-loader'],
                exclude: [
                    // Completely exclude entities package from source map processing
                    /node_modules\/entities\//,
                    // Also exclude highlight.js which has source map issues
                    /node_modules\/highlight\.js\//
                ]
            }
        ]
    }
};
