const webpack = require('webpack');
const path = require('path');
const autoprefixer = require('autoprefixer');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const PWD = __dirname;
const REGEX_PATH_SEP = process.platform === 'win32' ? '\\\\' : '\/';
const PRODUCTION = process.env.PRODUCTION;

const config = {};

/**************** RESOLVING NAMES ***************/
config.resolve = {
    alias: {
        'obshtestvo-ui': path.normalize(`${PWD}/obshtestvo-ui`), // @todo extract as npm module
        '.modernizrrc': path.normalize(`${PWD}/.modernizrrc`)
    },
    extensions: ['', '.js']
};
config.externals = {
    modernizr: 'var Modernizr'
};

/**************** INPUT ***************/
config.entry = {
    head: './src/head',
    app: './src/index',
    // the following "vendor" bundle is intentionally not including all dependencies, because:
    // 1) the project can rely only on parts of the dependencies
    // 2) dependencies also change, so we should only extract base dependencies that are unlikely to change
    vendor: [
        'react',
        'react-dom',
        'history/es6/createBrowserHistory',
        'history/es6/useQueries',
        'redux/src/createStore',
        'redux/src/applyMiddleware',
        'redux-thunk'
    ]
};

/**************** OUTPUT ***************/
config.output = {
    path: path.normalize(`${PWD}/build`),
    filename: '[name].js',
    publicPath: '/build/'
};

/**************** PLUGINS ***************/
config.plugins = [
    new webpack.ProvidePlugin({'React': 'react'}),
    new webpack.optimize.CommonsChunkPlugin({
        name: 'vendor',
        chunks: ['vendor', 'app']
    })
];
if (PRODUCTION) {
    config.plugins.push(new ExtractTextPlugin('[name].css'));
    //config.plugins.push(new webpack.optimize.DedupePlugin()); // this actually increases build size?
    config.plugins.push(new webpack.optimize.OccurrenceOrderPlugin(true));
    config.plugins.push(new webpack.optimize.UglifyJsPlugin({
        sourceMap: false,
        //mangle: ... this actually increases build size
        compress: {
            warnings: false,
            drop_console: true
        },
        output: {comments: false}
    }));
}

/**************** DEV TOOLS ***************/
if (!PRODUCTION) {
    config.devtool = 'eval-source-map';
}


/**************** MODULE LOADING ***************/
var svgExtraLoaders = '';
if (PRODUCTION) {
    svgExtraLoaders = '!svgo';
}
var ES6Roots = [
    `obshtestvo-ui`,
    `src`,
    'node_modules/react-templates/src',
    'node_modules/history/es6',
    'node_modules/redux/src'
].map(root => path.normalize(`${PWD}/${root}`)).join('|').replace(new RegExp(REGEX_PATH_SEP, 'g'), REGEX_PATH_SEP);
var getStylingLoader = function (additionalLoaders) {
    var cssOptions = {
        sourceMap: true,
        importLoaders: 1,
        modules: true,
        minimize: false
    };
    if (PRODUCTION) {
        cssOptions = {
            importLoaders: 1,
            discardComments: {removeAll: true},
            modules: true
        }
    }
    var loaders = ['style', `css?${JSON.stringify(cssOptions)}`, 'postcss'];
    if (additionalLoaders) loaders.push(additionalLoaders);
    if (!PRODUCTION) return loaders.join('!');
    return ExtractTextPlugin.extract(loaders[0], loaders.splice(1).join('!'))
};
var devBabelTransforms = [];
if (!PRODUCTION) {
    devBabelTransforms.push(['react-transform', {
        'transforms': [{
            'transform': 'react-transform-hmr',
            'imports': ['react'],
            'locals': ['module']
        }, {
            'transform': 'react-transform-catch-errors',
            'imports': ['react', 'redbox-react']
        }]
    }])
}
var skipProcessingLoader = 'imports?this=>window&module=>false&exports=>false&define=>false';
config.module = {
    //preLoaders:[
    //    {test: /\.js$/, loader: 'eslint', exclude: /node_modules/}
    //],
    loaders: [
        {
            test: /\.modernizrrc$/,
            loader: 'modernizr'
        },
        {
            test: /\.scss$/,
            loader: getStylingLoader('!sass?sourceMap')
        },
        {test: /\.css$/, loader: getStylingLoader()},
        {test: new RegExp(`autorequire${REGEX_PATH_SEP}.+$`), loader: 'file?name=auto/[name].[ext]'},
        {test: /^(?:(?!autorequire).)+\.gif$/, loader: 'url?limit=100000&mimetype=image/gif'},
        {test: /^(?:(?!autorequire).)+\.png$/, loader: 'url?limit=100000&mimetype=image/png'},
        {test: /^(?:(?!autorequire).)+\.jpg$/, loader: 'file'},
        {test: /\.woff$/, loader: 'url?limit=100000&mimetype=application/font-woff'},
        {test: /\.json$/, loader: 'json'},
        // if svg maximum optimization is required use dangerouslySetInnerHTML: http://stackoverflow.com/a/30845262/339872
        //{test: /\.svg$/, loader: 'raw'+svgExtraLoaders},
        {test: /\.svg$/, loader: 'babel?presets[]=react&presets[]=es2015!svg-jsx?es6=true' + svgExtraLoaders},
        {
            test: new RegExp('(:?' + ES6Roots + ').+\.jsx?$'),
            loader: 'babel',
            query: {
                cacheDirectory: true,
                plugins: [
                    'jsx-control-statements',
                    'transform-decorators-legacy',
                    'transform-class-properties',
                    'transform-object-assign',
                    'transform-object-rest-spread'
                ].concat(devBabelTransforms),
                presets: ['es2015', 'react']
            }
        }
    ]
};


/**************** POSTCSS module ***************/
config.postcss = [autoprefixer({
    browsers: [
        'Android 2.3',
        'Android >= 4',
        'Chrome >= 35',
        'Firefox >= 31',
        'Explorer >= 9',
        'iOS >= 7',
        'Opera >= 12',
        'Safari >= 7.1',
    ]
})];

/**************** File changes watching/monitoring options ***************/
config.watchOptions = {
    aggregateTimeout: 100
};

module.exports = config;
