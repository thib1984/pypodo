# 🙏 Thanks !

Oh if you open this page, it's for contributing for this project, great ! A big thanks 🙏

To contribute, it's simple, check the [existing issues](https://github.com/thib1984/pypodo/issues). If you see an issue you are interested to work, please let a message and i assign you the task. With this, all people know you are working on this issue.

If it's a new subject, don't hesitate to create an issue. I will check this one to affect some labels and let contribution open 😉

You can initialize a draft merge request directly when you start to work on an issue.

When you finish, past the merge request in "ready" mode and i will check this quickly.

If you are any questions, don't try to ping me 😁

# Local install to develop

git clone https://github.com/thib1984/pypodo.git
cd pypodo 
rm -rf pypodo_env #clean env if necessary
python3 -m venv pypodo_env
source pypodo_env/bin/activate
#work!
pip3 install .
pypodo [...] #to retest
deactivate

python3 -m build && python3 -m twine upload dist/* #to publish to pypi
