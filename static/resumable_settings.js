const place = document.querySelector(".resumable-drop, .resumable-browse");


var r = new Resumable({
    target: '/api/files/upload/chunks/',
    chunkSize: 50 * 1024 * 1024,
    simultaneousUploads: 4,
    testChunks: true,
    throttleProgressCallbacks: 1,
    query: {
        resumableHash: 'hashChunk',
        resumableDescription: 'description'
    }
});
// Resumable.js isn't supported, fall back on a different method
if (!r.support) {
    $('.resumable-error').show();
} else {
    // Show a place for dropping/selecting files
    $('.resumable-drop').show();
    r.assignDrop($('.resumable-drop')[0]);
    // r.assignBrowse($('.resumable-browse')[0]);

    // Handle file add event
    r.on('fileAdded', function (file) {
        // Show progress pabr
        $('.resumable-progress, .resumable-list').show();
        // Show pause, hide resume
        $('.resumable-progress .progress-resume-link').hide();
        $('.resumable-progress .progress-pause-link').show();
        // Add the file to the list
        $('.resumable-list').append('<li class="resumable-file-' + file.uniqueIdentifier + '">Uploading <span class="resumable-file-name"></span> <span class="resumable-file-progress"></span>');
        $('.resumable-file-' + file.uniqueIdentifier + ' .resumable-file-name').html(file.fileName);
        // Actually start the upload
        r.upload();
    });
    r.on('pause', function () {
        // Show resume, hide pause
        $('.resumable-progress .progress-resume-link').show();
        $('.resumable-progress .progress-pause-link').hide();
    });
    r.on('complete', function () {
        // Hide pause/resume when the upload has completed
        $('.resumable-progress .progress-resume-link, .resumable-progress .progress-pause-link').hide();
    });
    r.on('fileSuccess', function (file, message) {
        // Reflect that the file upload has completed
        $('.resumable-file-' + file.uniqueIdentifier + ' .resumable-file-progress').html('(completed)');
    });
    r.on('fileError', function (file, message) {
        // Reflect that the file upload has resulted in error
        $('.resumable-file-' + file.uniqueIdentifier + ' .resumable-file-progress').html('(file could not be uploaded: ' + message + ')');
    });
    r.on('fileProgress', function (file) {
        // Handle progress for both the file and the overall upload
        $('.resumable-file-' + file.uniqueIdentifier + ' .resumable-file-progress').html(Math.floor(file.progress() * 100) + '%');
        $('.progress-bar').css({width: Math.floor(r.progress() * 100) + '%'});
    });
    r.on('cancel', function () {
        $('.resumable-file-progress').html('canceled');
    });
    r.on('uploadStart', function () {
        // Show pause, hide resume
        $('.resumable-progress .progress-resume-link').hide();
        $('.resumable-progress .progress-pause-link').show();
    });
    XMLHttpRequest.prototype.open = (function (open) {
        return function (method, url, async) {
            open.apply(this, arguments);
            this.setRequestHeader('Access-Token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjdlYjEyOWQxLTFkZTUtNDJmNC05MTE2LWI1Mjc0NzA1YThlYyIsImV4cCI6MTY1MDQzOTM4N30.Z5KsORHlNFqpWWU30JkNIO9L8ed40d1NUpxOzQ36vXE');
        };
    })(XMLHttpRequest.prototype.open);
}

place.ondrop = function (event) {
    r.updateQuery({resumableDescription: document.getElementById("description-text").value})
};