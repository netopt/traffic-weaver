// commit-and-tag-version-updater.js

module.exports.readVersion = function (contents) {
    const regex = /version.*=.*["\'](.*)["\']/
    var match = contents.match(regex)
    return match[1].toString()
};

module.exports.writeVersion = function (contents, version) {
    const regex = /(version.*=.*["\'])(.*)(["\'])/
    contents = contents.replace(regex, "$1" + version + "$3")
    return contents
};