from bs4 import BeautifulSoup
import requests
import re

EVENT_MAPPING = {
    'edx.bookmark.added': 'edx_bookmark_added',
    'edx.bookmark.listed': 'edx_bookmark_listed',
    'edx.bookmark.accessed': 'edx_bookmark_accessed',
    'edx.bookmark.removed': 'edx_bookmark_removed',
    'edx.ui.lms.link_clicked': 'edx_ui_lms_link_clicked',
    'edx.course.enrollment.activated': 'edx_course_enrollment_activated',
    'edx.course.enrollment.deactivated': 'edx_course_enrollment_deactivated',
    'edx.course.enrollment.mode_changed':
        'edx_course_enrollment_mode_changed',
    'edx.course.enrollment.upgrade.clicked':
        'edx_course_enrollment_upgrade_clicked',
    'speed_change_video': 'edx_video_speed_changed',
    'edx.course.tool.accessed': 'edx_course_tool_accessed',
    'edx.forum.response.created': 'edx_forum_response_created',
    'problem_show': 'problem_show',
    'edx.ui.lms.sequence.next_selected': 'edx_ui_lms_sequence_next_selected',
    'edx.ui.lms.sequence.previous_selected':
        'edx_ui_lms_sequence_previous_selected',
    'seq_next': 'seq_next',
    'seq_prev': 'seq_prev',
    'stop_video': 'stop_video',
    'problem_graded': 'problem_graded',
    'problem_save': 'problem_save',
    'edx.grades.problem.submitted': 'edx_grades_problem_submitted',
    'edx.problem.hint.demandhint_displayed':
        'edx_problem_hint_demandhint_displayed',
    'edx.problem.hint.feedback_displayed':
        'edx_problem_hint_feedback_displayed',
    'pause_video': 'pause_video',
    'seek_video': 'seek_video',
    'load_video': 'load_video',
    'show_transcript': 'show_transcript',
    'edx.video.closed_captions.shown': 'edx_video_closed_captions_shown',
    'edx.video.closed_captions.hidden': 'edx_video_closed_captions_hidden',
    'video_show_cc_menu': 'video_show_cc_menu',
    'problem_reset': 'problem_reset',
    'seq_goto': 'seq_goto',
    'problem_rescore': 'problem_rescore',
    'edx.forum.thread.viewed': 'edx_forum_thread_viewed',
    'save_problem_success': 'save_problem_success',
    'play_video': 'play_video',
    'hide_transcript': 'hide_transcript',
    'video_hide_cc_menu': 'video_hide_cc_menu',
    'edx.forum.thread.created': 'edx_forum_thread_created',
    'openassessmentblock.get_peer_submission':
        'openassessmentblock_get_peer_submission',
    'openassessmentblock.peer_assess': 'openassessmentblock_peer_assess',
    'edx.course.student_notes.viewed': 'edx_course_student_notes_viewed',
    'textbook.pdf.page.navigated': 'textbook_pdf_page_navigated',
    'edx.forum.comment.created': 'edx_forum_comment_created',
    'xblock.poll.view_results': 'xblock_poll_view_results',
    'xblock.survey.view_results': 'xblock_survey_view_results',
    'openassessment.student_training_assess_example':
        'openassessment_student_training_assess_example',
    'xblock.survey.submitted': 'xblock_survey_submitted',
    'problem_check': 'problem_check',
    'openassessmentblock.create_submission':
        'openassessmentblock_create_submission',
    'xblock.poll.submitted': 'xblock_poll_submitted',
    'edx.course.student_notes.deleted': 'edx_course_student_notes_deleted',
    'edx.course.student_notes.edited': 'edx_course_student_notes_edited',
    'edx.course.student_notes.added': 'edx_course_student_notes_added',
    'openassessmentblock.get_submission_for_staff_grading':
        'openassessmentblock_get_submission_for_staff_grading',
    'textbook.pdf.page.scrolled': 'textbook_pdf_page_scrolled',
    'textbook.pdf.zoom.menu.changed': 'textbook_pdf_zoom_menu_changed',
    'textbook.pdf.thumbnail.navigated': 'textbook_pdf_thumbnail_navigated',
    'textbook.pdf.zoom.buttons.changed': 'textbook_pdf_zoom_buttons_changed',
    'book': 'book',
    'edx.course.enrollment.upgrade.succeeded':
        'edx_course_enrollment_upgrade_succeeded',
    'edx.course.student_notes.notes_page_viewed':
        'edx_course_student_notes_notes_page_viewed',
    'edx.cohort.user_added': 'edx_cohort_user_added',
    'edx.forum.thread.voted': 'edx_forum_thread_voted',
    'edx.forum.response.voted': 'edx_forum_response_voted',
    'openassessmentblock.submit_feedback_on_assessments':
        'openassessmentblock_submit_feedback_on_assessments',
    'openassessmentblock.save_submission':
        'openassessmentblock_save_submission',
    'edx.googlecomponent.document.displayed':
        'edx_googlecomponent_document_displayed',
    'edx.googlecomponent.calendar.displayed':
        'edx_googlecomponent_calendar_displayed',
    'openassessmentblock.staff_assess': 'openassessmentblock_staff_assess',
    'edx.forum.searched': 'edx_forum_searched',
    'oppia.exploration.state.changed': 'oppia_exploration_state_changed',
    'textbook.pdf.search.executed': 'textbook_pdf_search_executed',
    'openassessmentblock.self_assess': 'openassessmentblock_self_assess',
    'edx.drag_and_drop_v2.item.dropped': 'edx_drag_and_drop_v2_item_dropped',
    'edx.drag_and_drop_v2.item.picked_up':
        'edx_drag_and_drop_v2_item_picked_up',
    'oppia.exploration.loaded': 'oppia_exploration_loaded',
    'ubc.peer_instruction.original_submitted':
        'ubc_peer_instruction_original_submitted',
    'ubc.peer_instruction.revised_submitted':
        'ubc_peer_instruction_revised_submitted',
    'edx.drag_and_drop_v2.loaded': 'edx_drag_and_drop_v2_loaded',
    'edx.team.changed': 'edx_team_changed',
    'edx.course.home.resume_course.clicked':
        'edx_course_home_resume_course_clicked',
    'edx.special_exam.timed.attempt.created':
        'edx_special_exam_timed_attempt_created',
    'edx.special_exam.timed.attempt.started':
        'edx_special_exam_timed_attempt_started',
    'edx.course.student_notes.used_unit_link':
        'edx_course_student_notes_used_unit_link',
    'edx.special_exam.timed.attempt.submitted':
        'edx_special_exam_timed_attempt_submitted',
    'edx.drag_and_drop_v2.feedback.opened':
        'edx_drag_and_drop_v2_feedback_opened',
    'edx.drag_and_drop_v2.feedback.closed':
        'edx_drag_and_drop_v2_feedback_closed',
    'edx.special_exam.timed.attempt.ready_to_submit':
        'edx_special_exam_time_attempt_ready_to_submit',
    'edx.cohort.created': 'edx_cohort_created',
    'edx.special_exam.practice.attempt.created':
        'edx_special_exam_practice_attempt_created',
    'edx.cohort.user_removed': 'edx_cohort_user_removed',
    'edx.team.page_viewed': 'edx_team_page_viewed',
    'edx.grades.problem.state_deleted': 'edx_grades_problem_state_deleted',
    'edx.grades.problem.rescored': 'edx_grades_problem_rescored',
    'reset_problem_fail': 'reset_problem_fail',
    'edx.grades.problem.score_overridden':
        'edx_grades_problem_score_overridden',
    'edx.team.learner_added': 'edx_team_learner_added',
    'reset_problem': 'reset_problem',
    'showanswer': 'showanswer',
    'edx.special_exam.timed.attempt.deleted':
        'edx_special_exam_timed_attempt_deleted',
    'textbook.pdf.outline.toggled': 'textbook_pdf_outline_toggled',
    'oppia.exploration.completed': 'oppia_exploration_completed',
    'edx.team.searched': 'edx_team_searched',
    'textbook.pdf.search.highlight.toggled':
        'textbook_pdf_search_highlight_toggled',
    'textbook.pdf.searchcasesensitivity.toggled':
        'textbook_pdf_searchcasesensitivity_toggled',
    'edx.course.student_notes.searched': 'edx_course_student_notes_searched',
    'edx.user.settings.viewed': 'edx_user_settings_viewed',
    'textbook.pdf.thumbnails.toggled': 'textbook_pdf_thumbnails_toggled',
    'edx.team.deleted': 'edx_team_deleted',
    'edx.team.created': 'edx_team_created',
    'ubc.peer_instruction.accessed': 'ubc_peer_instruction_accessed',
    'problem_check_fail': 'problem_check_fail',
    'textbook.pdf.display.scaled': 'textbook_pdf_display_scaled',
    'textbook.pdf.chapter.navigated': 'textbook_pdf_chapter_navigated',
    'textbook.pdf.search.navigatednext':
        'textbook_pdf_search_navigatednext',
    'edx.certificate.created': 'edx_certificate_created',
    'edx.librarycontentblock.content.removed':
        'edx_librarycontentblock_content_removed',
    'edx.user.settings.changed': 'edx_user_settings_changed',
    'xmodule.partitions.assigned_user_to_partition':
        'xmodule_partitions_assigned_user_to_partition',
    'openassessmentblock.save_files_descriptions':
        'openassessmentblock_save_files_descriptions',
    'xblock.split_test.child_render': 'xblock_split_test_child_render',
    'edx.librarycontentblock.content.assigned':
        'edx_librarycontentblock_content_assigned',
    'edx.bi.course.upgrade.sidebarupsell.displayed':
        'edx_bi_course_upgrade_sidebarupsell_displayed',
    'save_problem_fail': 'save_problem_fail',
    'edx.team.learner_removed': 'edx_team_learner_removed',
    'edx.team.activity_updated': 'edx_team_activity_updated',
    'edx.special_exam.proctored.created': 'edx_special_exam_proctored_created',
    'edx.special_exam.practice.created': 'edx_special_exam_practice_created',
    'edx.done.toggled': 'edx_done_toggled',
    'edx.special_exam.practice.updated': 'edx_special_exam_practice_updated',
    'edx.special_exam.timed.updated': 'edx_special_exam_timed_updated',
    'edx.special_exam.proctored.updated': 'edx_special_exam_proctored_updated',
    'edx.special_exam.timed.created': 'edx_special_exam_timed_created',
    'edx.grades.grading_policy_changed': 'edx_grades_grading_policy_changed',
    'page_close': 'page_close',
    'edx.certificate.evidence_visited': 'edx_certificate_evidence_visited',
    'edx.certificate.shared': 'edx_certificate_shared',
    'edx.cohort.creation_requested': 'edx_cohort_creation_requested',
    'edx.cohort.user_add_requested': 'edx_cohort_user_add_requested',
    'edx.user.login': 'edx_user_login',
    'edx.user.logout': 'edx_user_logout',
}


url='https://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/tracking_logs/student_event_types.html'
transformed = []
not_transformed = []

#resp = requests.get('https://edx.readthedocs.io/projects/devdata/en/stable/internal_data_formats/tracking_logs.html')
print('Tranformed and documented')
resp = requests.get(url)
content = BeautifulSoup(resp.content, "html.parser")
mydivs = content.findAll("a", {"class": "toc-backref"})
for a in mydivs:
    link=a['href']
    spans=a.findAll("span", {"class": "pre"})
    if spans:
        for span in spans:
            event=span.text
            e=content.findAll("span",text=event)[0]
            try:
                event_url=e.parent.parent.get('href')
            except:
                event_url=""
            
            if event_url:
                event_url =  url+event_url
            else:
                event_url = url

            if event in EVENT_MAPPING.keys():
                transformed.append(event)
                print("* {0}".format(event))
                #print("* `{0} <{1}>`_".format(event, event_url))
                #print("documented")
                del EVENT_MAPPING[event]
            else:
                if event not in transformed and event not in not_transformed:
                    not_transformed.append(event)
                pass  
    #import pdb;pdb.set_trace();
    #print(i)


print("===================================>>>>>>>>>>>>>>>>>>>>>>>")
print('Tranformed but not documented')
abc=[]
for i in EVENT_MAPPING.keys():
    abc.append("* {0}".format(i))

abc.sort()

for i in abc:
    print(i)

print("===================================>>>>>>>>>>>>>>>>>>>>>>>")
print('Not Transformed')
for v in not_transformed:
	print("* {0}".format(v))