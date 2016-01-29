export function getHost(url) {
    url = url.split('//');
    if (url.length == 1 || url[0].indexOf('/') > -1) return false;
    return url[1].split('/')[0];
}

export function removePath(url) {
    var [protocol, hostWithPath] = url.split('://');
    hostWithPath = hostWithPath.slice(0, hostWithPath.indexOf('/'))
    return [protocol, hostWithPath].join('://')
}