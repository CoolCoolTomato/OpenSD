import devConfig from './config.development.js';
import prodConfig from './config.production.js';

let Config;

if (process.env.NODE_ENV === 'development') {
    Config = devConfig;
} else if (process.env.NODE_ENV === 'production') {
    Config = prodConfig;
} else {
    throw new Error('NODE_ENV not set or invalid');
}

export default Config;