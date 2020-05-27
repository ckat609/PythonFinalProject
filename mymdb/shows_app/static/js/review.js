function showAddReview() {
    contentA = `
        <form action="/shows/review/add" method="post">
    `
    contentB = `
            <div class="form-group">
                <input type="hidden" name="show_id" value="{{show.id}}">
                <label for="review_title">Title</label>
                <input type="text" name="review_title" id="review_title" class="form-control">
            </div>
            <div class="form-group">
            <label for="review_score">Score</label>
                <select class="form-control" id="review_score" name="review_score">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option selected>5</option>
                </select>
            </div>
            <div class="form-group">
                <label for="review_text">Review</label>
                <textarea name="review_text" id="" cols="30" rows="5" class="form-control"></textarea>
            </div>
            <div class="form-group float-right">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form>
    `
    document.getElementById("add_review").innerHTML = contentA + document.getElementById("add_review").innerHTML + contentB
    console.log(contentA + document.getElementById("add_review").innerHTML + contentB)
}