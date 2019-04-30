# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from redisUtils import RedisStream



# App config.
DEBUG = True
#static_folder='/opt/static'
#template_folder="/opt/templates"
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
redis_queue = os.environ.get('WAIT_QUEUE', "demo_wait_q_0")


r = RedisStream()


class ReusableForm(Form):
    task = TextField('Task:', validators=[validators.required(), validators.Length(min=1)])

@app.route("/", methods=['GET', 'POST'])
def run():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        task=request.form['task']
        print(task)
        if form.validate():
            # Save the comment here.
            flash('Thanks for your task: ' + task)
            r.pushTask(redis_queue, task)
        else:
            flash('Error: WTF is your task?')

    return render_template('form.html', form=form)



def main():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
