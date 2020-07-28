"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from web_fragments.fragment import Fragment

from xblock.core import XBlock
from xblock.scorable import ScorableXBlockMixin, Score


from xblock.fields import Integer, Scope, UNSET
from django.utils.safestring import SafeText
import textwrap
import urllib
import json
import random

@XBlock.wants('user')
class Goss4XBlock(ScorableXBlockMixin, XBlock):
    """
    XBlock checks if a certain URL returns what is expected 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    #package = __package__
    always_recalculate_grades = True
    
    score2 = Integer(
        default=UNSET, scope=Scope.user_state,
        help="An indicator of success",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def has_submitted_answer(self):
        """
        Returns True if the user has made a submission.
        """
        return self.fields['score2'].is_set_on(self)

    def max_score(self):  # pylint: disable=no-self-use
        """
        Return the problem's max score
        Required by the grading system in the LMS.
        """
        return 100
    
    def set_score(self, score):
        """
        Sets the score on this block.
        Takes a Score namedtuple containing a raw
        score and possible max (for this block, we expect that this will
        always be 1).
        """
        #assert score.raw_possible == self.max_score()
        self.score2 = score.raw_earned

    def get_score(self):
        """
        Return the problem's current score as raw values.
        """
        
        return Score(self.score2, self.max_score())

    def calculate_score(self):
        """
        Returns a newly-calculated raw score on the problem for the learner
        based on the learner's current state.
        """
        return Score(self.score2, self.max_score())


    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the Goss2XBlock, shown to students
        when viewing courses.
        """
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        CURRENT = xb_user.opt_attrs.get('edx-platform.username')

        XURL = 'https://fork.kodaktor.ru/testxblock2'
        response = urllib.urlopen(XURL)
        data = json.loads(response.read())
        CHECK = data['message']

        html = self.resource_string("static/html/goss4xblock.html")
        frag = Fragment(html.format(self=self))

        res = textwrap.dedent("""
            <h2>X4a: Server app challenge</h2>
            <p>Your server app URL should return this: <span id="gosscurrent">{}</span>!</h2>
            <p>The address {} returned {}</h2>
            <div>Enter URL: <input id='gossinput' /><br/>
            <button id='gosssend'>send to server</button>
            </div> 
        """).format(CURRENT, XURL, CHECK)
        frag.add_content(SafeText(res))

        frag.add_css(self.resource_string("static/css/goss4xblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/goss4xblock.js"))
        frag.initialize_js('Goss4XBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def set_score2(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # indicator is now 100...
        if data['key'] == 'hundred':
             self.score2 = 100
        else:
             self.score2 = 0

        self._publish_grade(Score(self.score2, self.max_score()))

        url = "https://fork.kodaktor.ru/publog3?EDXEDX-4---------"
        urllib.urlopen(url+'score --- published')        
        return {"score": self.score2}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Goss4XBlock",
             """<problem/>
             """),
            ("Multiple Goss4XBlock",
             """<vertical_demo>
                <goss2xblock/>
                <goss2xblock/>
                <goss2xblock/>
                </vertical_demo>
             """),
        ]

