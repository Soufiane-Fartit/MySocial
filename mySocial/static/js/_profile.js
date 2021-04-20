function addFriend(id) {
    $.ajaxSetup({async: false});
    console.log('adding friend ', id);
    $.post('/addfriend', {'user_id': id},function(data) {});
    location.reload();
}
function confirmRelation(id) {
    $.ajaxSetup({async: false});
    console.log('confirming relation ', id);
    $.post('/confirmrelation', {'user_id': id},function(data) {});
    location.reload();
}
function rejectRelation(id) {
    $.ajaxSetup({async: false});
    console.log('rejecting relation ', id);
    $.post('/rejectrelation', {'user_id': id},function(data) {});
    location.reload();
}
function sendNewPost(id) {
    $.ajaxSetup({async: false}); 
    var new_post = $("#new-post").val();
    console.log('sending new post ', new_post);
    $.post('/newpost', {'text': new_post},function(data) {});
}
function deletePost(id) {
    console.log('deleting post ', id);
    $.post('/deletepost', {'post_id': id},function(data) {});
    location.reload();
}
function showCommentField(id) {
    $.ajaxSetup({async: false}); 
    console.log('comment button clicked', id);
    var x = document.getElementById("comment-field-"+String(id));
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
  function sendComment(id) {
      var comment = $("#comment-"+String(id)).val();
      console.log('sending comment for ', id, '==>', comment);
      $.post('/comment', {'post_id': id, 'text': comment},function(data) {});
  }
  function sharePost(id) {
      console.log('sharing post ', id);
      $.post('/sharepost', {'post_id': id},function(data) {});
  }
