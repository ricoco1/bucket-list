$(document).ready(function() {
    show_bucket();
});

function show_bucket() {
    $('#bucket-list').empty()
    $.ajax({
        type: "GET",
        url: "/bucket",
        data: {},
        success: function(response) {
            let rows = response['buckets']
            
            // Cek jika data kosong
            if (rows.length === 0) {
                $('#bucket-list').append('<h2>Bucket list masih kosong!!</h2>');
            } else {
                for (let i = 0; i < rows.length; i++) {
                    let bucket = rows[i]['bucket']
                    let num = rows[i]['num']
                    let done = rows[i]['done']

                    let temp_html = ''
                    if (done === 0) {
                        temp_html = `<li>
                                <h2>✅ ${bucket}</h2>
                                <button onclick="done_bucket(${num})" type="button" class="btn btn-outline-primary">✅ Done</button>
                                <button onclick="delete_bucket(${num})" type="button" class="btn btn-outline-danger" style="margin-left: 10px;">❌ Delete</button>
                            </li>`
                    } else {
                        temp_html = `<li>
                                <h2 class="done">✅ ${bucket}</h2>
                            </li>`
                    }
                    $('#bucket-list').append(temp_html)
                }
            }
        }
    });
}

function save_bucket() {
    let bucket = $('#bucket').val()

    // cek apakah input data kosong
    if (bucket.trim() === '') {
        Swal.fire({
            title: 'Notification',
            text: 'Bucket tidak boleh kosong!',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    } else {
        let spinner = new Spinner().spin();
        $('#loading').append(spinner.el);
        $.ajax({
            type: "POST",
            url: "/bucket",
            data: {
                bucket_give: bucket
            },
            success: function(response) {
                spinner.stop();
                Swal.fire({
                    title: 'Notification',
                    text: response["msg"],
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload();
                    }
                });
            }
        });
    }
}

function done_bucket(num) {
    $.ajax({
        type: "POST",
        url: "/bucket/done",
        data: {
            'num_give': num
        },
        success: function(response) {
            Swal.fire({
                title: 'Notification',
                text: response["msg"],
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });
        }
    });
}

function delete_bucket(num) {
    Swal.fire({
        title: 'Confirmation',
        text: 'Are you sure you want to delete this item?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: "/bucket/delete",
                data: {
                    'num_give': num
                },
                success: function(response) {
                    Swal.fire({
                        title: 'Notification',
                        text: response["msg"],
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.reload();
                        }
                    });
                },
                error: function(xhr, status, error) {
                    Swal.fire({
                        title: 'Error',
                        text: 'Failed to delete item. Please try again.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            });
        }
    });
}