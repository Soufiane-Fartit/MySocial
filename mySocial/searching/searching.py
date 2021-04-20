from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Relations
from .. import db

searching = Blueprint('searching', __name__, template_folder='templates')

@searching.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        searched_term = request.form['searched_term']
        if searched_term.isdigit():
            candidate_users = [User.query.get(searched_term)]
        else:
            searched_words = searched_term.split(' ')
            candidate_users = []
            for searched_word in searched_words:
                possible_matches = User.query.filter(User.first_name==searched_word).all() + User.query.filter(User.last_name==searched_word).all()
                candidate_users = candidate_users + possible_matches
            candidate_users = list(set(candidate_users))
        print(candidate_users)

        current_user_friends_id_list = [x.user2_id for x in Relations.query.filter(Relations.user1_id==current_user.id).all()] \
                                    + [x.user1_id for x in Relations.query.filter(Relations.user2_id==current_user.id).all()]
        for x in candidate_users:
            if x.id != current_user.id:
                if x.id in current_user_friends_id_list :
                    x.is_friend = 1
                else :
                    x.is_friend = 0
            else:
                x.is_friend = 1
        return render_template('searching/search.html', searched_term=searched_term, candidate_users=candidate_users, connected_id=current_user.id)

    return render_template('searching/search.html', connected_id=current_user.id)