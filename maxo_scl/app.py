from flask import Flask, render_template, request, url_for, redirect, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
@app.route('/login', methods=["post", "get"])
def login():
    if 'loginusername' in request.form and 'loginpassword' in request.form:
        user = request.form['loginusername']
        password = request.form['loginpassword']
        if user == "" or password == "":
            flash("Fields shouldnt be left empty")
            return redirect(url_for('login'))
        try:

            db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya", password="888000++vVvV",
                                 autocommit=True)
            cur = db.cursor()

            ab = "use achintya_maxo_scl"
            cur.execute(ab)
            query = "select User_password,User_Email from userdetails where User_name=%s"
            cur.execute(query, (user))
            answer_in_tuple_form = cur.fetchone()

            if answer_in_tuple_form == None:
                flash("User Doesnt exists")
                db.close()
                return redirect(url_for('login'))
            else:
                answer = answer_in_tuple_form[0]
                email = answer_in_tuple_form[1]
                if answer == password:
                    session['user'] = user
                    session['email'] = email

                    ab = "use achintya_maxo_scl"
                    cur.execute(ab)
                    a = "show columns from December"
                    cur.execute(a)
                    columns_tuple = cur.fetchall()
                    columns_list = []
                    columns_of_languages = []
                    for i in columns_tuple:
                        if i[0] == "Linkid":
                            continue
                        columns_list.append(i[0])

                    language_start = columns_list.index('Languagelink')
                    language_end = columns_list.index('Improvelink')
                    columns_of_languages = columns_list[language_start + 1:language_end]
                    session['columns_of_languages'] = columns_of_languages

                    improve_start = columns_list.index('Improvelink')
                    improve_stop = columns_list.index('Artlink')
                    improve_columns = columns_list[improve_start + 1:improve_stop]
                    session['improve_columns'] = improve_columns

                    art_start = columns_list.index('Artlink')
                    art_stop = len(columns_list)
                    art_columns = columns_list[art_start + 1:art_stop]
                    session['art_columns'] = art_columns

                    db.close()
                    return render_template('mainpage.html', user=user)
                else:
                    db.close()
                    flash("Invalid  Password!!!")
                    return redirect(url_for('login'))

        except pymysql.err.OperationalError as e:
            flash("Please Check your Connection")
        except Exception as e:
            print(e)
            if db.open:
                db.close()
            flash(e)
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=["post", "get"])
def register():
    if 'email' in request.form and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form:
        email = request.form['email']
        username = request.form['username']
        new_password = request.form['password']
        confirm_password = request.form['cpassword']
        print(email)
        print(username)
        print(new_password)
        if email == "" or username == "" or new_password == "" or confirm_password == "":
            flash("No fields should be left empty")
            return redirect(url_for('register'))  # To return to same page if any1 paramaters are left empty
        if new_password != confirm_password:
            flash("Passwords didnt match!!!")
            return redirect(url_for('register'))  # Return to same page if password doesnt match.

        try:
            db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya", password="888000++vVvV",
                                 autocommit=True)
            cur = db.cursor()

            ab = "use achintya_maxo_scl"
            cur.execute(ab)

            ab = "insert into userdetails (User_Email,User_name,User_password) values (%s,%s,%s)"
            cur.execute(ab, (email, username, new_password))
            db.close()
            return render_template('login.html')
        except Exception as e:
            db.close()
            flash(e)
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/forgotpassword')
def forgot_password():
    return render_template('forgotpassword.html')


@app.route('/mainpage', methods=['post', 'get'])
def mainpage():
    if 'language' in request.form:
        print("inside")
        language = request.form['language']

        print('inside1')

        if language == "language":
            columns_of_languages = session['columns_of_languages']
            print('inside2')
            return render_template('mainpage_nextpage.html', columns_of_languages=columns_of_languages)

        return redirect(url_for('mainpage'))

    elif 'improve' in request.form:
        improve_columns = session['improve_columns']
        return render_template('mainpage_nextpage.html', columns_of_languages=improve_columns)

    elif 'art' in request.form:
        art_columns = session['art_columns']
        return render_template('mainpage_nextpage.html', columns_of_languages=art_columns)

    return render_template('mainpage.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/nextpage', methods=['post', 'get'])
def nextpage():
    columns_of_languages = session['columns_of_languages']
    improve_link = session['improve_columns']
    art_link = session['art_columns']

    #     global columns_of_languages
    for i in columns_of_languages:
        if i in request.form:
            button_name = request.form[i]
            print(button_name)
            if button_name != "":
                try:
                    db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya",
                                         password="888000++vVvV", autocommit=True)
                    cur = db.cursor()
                    ab = "use achintya_maxo_scl"
                    cur.execute(ab)
                    a = f"select {button_name} from December"
                    cur.execute(a)
                    link_tuple = cur.fetchall()
                    linklist = []
                    for i in link_tuple:
                        if i[0] == None:
                            continue
                        else:
                            linklist.append(i[0])

                    top_property = []
                    first_value = 40
                    for i in range(0, len(linklist)):
                        top_property.append(first_value)
                        first_value = first_value + 540
                    link_with_topvalue = {}
                    print(linklist)
                    print(top_property)
                    for i in range(0, len(linklist)):
                        link_with_topvalue[linklist[i]] = top_property[i]

                    db.close()
                    return render_template('language1.html', link_with_topvalue=link_with_topvalue,
                                           button_name=button_name)

                except pymysql.err.OperationalError:
                    return redirect(url_for('nextpage'))
                except Exception as e:
                    print(e)
                    if db.open:
                        db.close()
                    return redirect(url_for('nextpage'))

    for i in improve_link:
        if i in request.form:
            button_name = request.form[i]
            print(button_name)
            if button_name != "":
                try:
                    db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya",
                                         password="888000++vVvV", autocommit=True)
                    cur = db.cursor()
                    ab = "use achintya_maxo_scl"
                    cur.execute(ab)
                    a = f"select {button_name} from December"
                    cur.execute(a)
                    link_tuple = cur.fetchall()
                    linklist = []
                    for i in link_tuple:
                        if i[0] == None:
                            continue
                        else:
                            linklist.append(i[0])

                    top_property = []
                    first_value = 40
                    for i in range(0, len(linklist)):
                        top_property.append(first_value)
                        first_value = first_value + 540
                    link_with_topvalue = {}
                    print(linklist)
                    print(top_property)
                    for i in range(0, len(linklist)):
                        link_with_topvalue[linklist[i]] = top_property[i]

                    db.close()
                    return render_template('language1.html', link_with_topvalue=link_with_topvalue,
                                           button_name=button_name)

                except pymysql.err.OperationalError:
                    return redirect(url_for('nextpage'))
                except Exception as e:
                    print(e)
                    if db.open:
                        db.close()
                    return redirect(url_for('nextpage'))

    for i in art_link:
        if i in request.form:
            button_name = request.form[i]
            print(button_name)
            if button_name != "":
                try:
                    db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya",
                                         password="888000++vVvV", autocommit=True)
                    cur = db.cursor()
                    ab = "use achintya_maxo_scl"
                    cur.execute(ab)
                    a = f"select {button_name} from December"
                    cur.execute(a)
                    link_tuple = cur.fetchall()
                    linklist = []
                    for i in link_tuple:
                        if i[0] == None:
                            continue
                        else:
                            linklist.append(i[0])

                    top_property = []
                    first_value = 40
                    for i in range(0, len(linklist)):
                        top_property.append(first_value)
                        first_value = first_value + 540
                    link_with_topvalue = {}
                    print(linklist)
                    print(top_property)
                    for i in range(0, len(linklist)):
                        link_with_topvalue[linklist[i]] = top_property[i]

                    db.close()
                    return render_template('language1.html', link_with_topvalue=link_with_topvalue,
                                           button_name=button_name)

                except pymysql.err.OperationalError:
                    return redirect(url_for('nextpage'))
                except Exception as e:
                    print(e)
                    if db.open:
                        db.close()
                    return redirect(url_for('nextpage'))

    return render_template('mainpage_nextpage.html', columns_of_languages=columns_of_languages)


@app.route('/language1')
def language1():
    return render_template('language1.html')


@app.route('/profile', methods=['post', 'get'])
def profile():
    present_username = session['user']
    present_email = session['email']

    return render_template('profile.html', name=present_username, email=present_email, user=present_username)


@app.route('/profile1', methods=['post', 'get'])
def profile1():
    if 'loginusername1' in request.form or 'email1' in request.form:

        changed_username = request.form['loginusername1']
        changed_email = request.form['email1']
        #         if changed_username!='' or changed_email!='':
        try:
            db = pymysql.connect(host="achintya.heliohost.us", user="achintya_achintya", password="888000++vVvV",
                                 autocommit=True)
            cur = db.cursor()
            ab = "use achintya_maxo_scl"
            cur.execute(ab)
            present_user = session['user']
            if changed_email != "" and changed_username != "":
                query = "update userdetails set User_name=%s,User_Email=%s where User_name=%s"
                cur.execute(query, (changed_username, changed_email, present_user))
                session.pop('user')
                session.pop('email')
                session['user'] = changed_username
                session['email'] = changed_email

            elif changed_email != "" and changed_username == "":
                query = "update userdetails set User_Email=%s where User_name=%s"
                cur.execute(query, (changed_email, present_user))
                session.pop('email')
                session['email'] = changed_email
            elif changed_email == "" and changed_username != "":
                query = "update userdetails set User_name=%s where User_name=%s"
                cur.execute(query, (changed_username, present_user))
                session.pop('user')
                session['user'] = changed_username

            present_username = session['user']
            present_email = session['email']

            db.close()
            return render_template('profile.html', name=present_username, email=present_email, user=present_username)


        except pymysql.err.OperationalError:
            flash('Check your Network')
            present_username = session['user']
            present_email = session['email']
            return render_template('profile.html', name=present_username, email=present_email, user=present_username)

        except Exception as e:
            flash(e)
            if db.open:
                db.close()
            present_username = session['user']
            present_email = session['email']

            return render_template('profile.html', name=present_username, email=present_email, user=present_email)

    present_username = session['user']
    present_email = session['email']
    print(present_username, present_email)

    return render_template('profile.html', name=present_username, email=present_email, user=present_username)


if __name__ == "__main__":
    app.run(host="localhost", port="5000")