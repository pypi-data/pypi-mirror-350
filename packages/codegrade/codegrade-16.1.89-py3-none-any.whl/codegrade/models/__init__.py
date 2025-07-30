"""Contains all the data models used in inputs/outputs.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

from ._base_price import _BasePrice
from ._saml_ui_logo_info import _SamlUiLogoInfo
from ._submission_rubric_item_data_parser import (
    _SubmissionRubricItemDataParser,
)
from .about import About
from .abstract_role import AbstractRole
from .access_token_modal_warning_time_setting import (
    AccessTokenModalWarningTimeSetting,
)
from .access_token_toast_warning_time_setting import (
    AccessTokenToastWarningTimeSetting,
)
from .add_users_section_data import AddUsersSectionData
from .ai_assistant_enabled_setting import AiAssistantEnabledSetting
from .all_auto_test_results import AllAutoTestResults
from .all_site_settings import AllSiteSettings
from .always_update_pii_with_lti_setting import AlwaysUpdatePiiWithLtiSetting
from .analytics_enabled_setting import AnalyticsEnabledSetting
from .any_auto_test_step_as_json import AnyAutoTestStepAsJSON
from .any_error import AnyError
from .any_non_redacted_auto_test_step_as_json import (
    AnyNonRedactedAutoTestStepAsJSON,
)
from .any_redacted_auto_test_step_as_json import AnyRedactedAutoTestStepAsJSON
from .api_codes import APICodes
from .assignment import Assignment
from .assignment_anonymization_algo import AssignmentAnonymizationAlgo
from .assignment_default_grading_scale_points_setting import (
    AssignmentDefaultGradingScalePointsSetting,
)
from .assignment_default_grading_scale_setting import (
    AssignmentDefaultGradingScaleSetting,
)
from .assignment_description_enabled_setting import (
    AssignmentDescriptionEnabledSetting,
)
from .assignment_description_on_teachers_submissions_page_setting import (
    AssignmentDescriptionOnTeachersSubmissionsPageSetting,
)
from .assignment_done_type import AssignmentDoneType
from .assignment_export_column import AssignmentExportColumn
from .assignment_feedback import AssignmentFeedback
from .assignment_grader import AssignmentGrader
from .assignment_grading_scale_points_enabled_setting import (
    AssignmentGradingScalePointsEnabledSetting,
)
from .assignment_kind import AssignmentKind
from .assignment_login_link import AssignmentLoginLink
from .assignment_max_points_enabled_setting import (
    AssignmentMaxPointsEnabledSetting,
)
from .assignment_peer_feedback_connection import (
    AssignmentPeerFeedbackConnection,
)
from .assignment_peer_feedback_settings import AssignmentPeerFeedbackSettings
from .assignment_percentage_decimals_setting import (
    AssignmentPercentageDecimalsSetting,
)
from .assignment_percentage_grading_settings import (
    AssignmentPercentageGradingSettings,
)
from .assignment_point_decimals_setting import AssignmentPointDecimalsSetting
from .assignment_points_grading_settings import AssignmentPointsGradingSettings
from .assignment_section_timeframe import AssignmentSectionTimeframe
from .assignment_state_enum import AssignmentStateEnum
from .assignment_submission_mode import AssignmentSubmissionMode
from .assignment_template import AssignmentTemplate
from .assignment_timeframes import AssignmentTimeframes
from .assistant_tools_enabled_setting import AssistantToolsEnabledSetting
from .at_image_caching_enabled_setting import AtImageCachingEnabledSetting
from .auto_test import AutoTest
from .auto_test_capture_points_message_setting import (
    AutoTestCapturePointsMessageSetting,
)
from .auto_test_checkpoint_message_setting import (
    AutoTestCheckpointMessageSetting,
)
from .auto_test_code_quality_message_setting import (
    AutoTestCodeQualityMessageSetting,
)
from .auto_test_enabled_setting import AutoTestEnabledSetting
from .auto_test_fixture import AutoTestFixture
from .auto_test_global_setup_output import AutoTestGlobalSetupOutput
from .auto_test_global_setup_script import AutoTestGlobalSetupScript
from .auto_test_heartbeat_interval_setting import (
    AutoTestHeartbeatIntervalSetting,
)
from .auto_test_heartbeat_max_missed_setting import (
    AutoTestHeartbeatMaxMissedSetting,
)
from .auto_test_io_test_message_setting import AutoTestIoTestMessageSetting
from .auto_test_io_test_sub_message_setting import (
    AutoTestIoTestSubMessageSetting,
)
from .auto_test_max_concurrent_batch_runs_setting import (
    AutoTestMaxConcurrentBatchRunsSetting,
)
from .auto_test_max_global_setup_time_setting import (
    AutoTestMaxGlobalSetupTimeSetting,
)
from .auto_test_max_jobs_per_runner_setting import (
    AutoTestMaxJobsPerRunnerSetting,
)
from .auto_test_max_per_student_setup_time_setting import (
    AutoTestMaxPerStudentSetupTimeSetting,
)
from .auto_test_max_result_not_started_setting import (
    AutoTestMaxResultNotStartedSetting,
)
from .auto_test_max_time_command_setting import AutoTestMaxTimeCommandSetting
from .auto_test_max_unit_test_metadata_length_setting import (
    AutoTestMaxUnitTestMetadataLengthSetting,
)
from .auto_test_quality_comment import AutoTestQualityComment
from .auto_test_result import AutoTestResult
from .auto_test_result_state import AutoTestResultState
from .auto_test_result_with_extra_data import AutoTestResultWithExtraData
from .auto_test_run import AutoTestRun
from .auto_test_run_program_message_setting import (
    AutoTestRunProgramMessageSetting,
)
from .auto_test_runner import AutoTestRunner
from .auto_test_runner_state import AutoTestRunnerState
from .auto_test_set import AutoTestSet
from .auto_test_step_base import AutoTestStepBase
from .auto_test_step_base_as_json import AutoTestStepBaseAsJSON
from .auto_test_step_base_input_as_json import AutoTestStepBaseInputAsJSON
from .auto_test_step_log_base import AutoTestStepLogBase
from .auto_test_step_result import AutoTestStepResult
from .auto_test_step_result_state import AutoTestStepResultState
from .auto_test_step_validation_exception import (
    AutoTestStepValidationException,
)
from .auto_test_suite import AutoTestSuite
from .auto_test_unit_test_message_setting import AutoTestUnitTestMessageSetting
from .automatic_lti1p3_assignment_import_setting import (
    AutomaticLti1p3AssignmentImportSetting,
)
from .automatic_lti_role_enabled_setting import AutomaticLtiRoleEnabledSetting
from .base_about import BaseAbout
from .base_auto_test_quality_comment import BaseAutoTestQualityComment
from .base_comment_base import BaseCommentBase
from .base_comment_base_with_extended_replies import (
    BaseCommentBaseWithExtendedReplies,
)
from .base_comment_base_with_normal_replies import (
    BaseCommentBaseWithNormalReplies,
)
from .base_comment_reply import BaseCommentReply
from .base_course_coupon import BaseCourseCoupon
from .base_directory import BaseDirectory
from .base_error import BaseError
from .base_file import BaseFile
from .base_lms_capabilities import BaseLMSCapabilities
from .base_lti1p1_provider import BaseLTI1p1Provider
from .base_lti1p3_provider import BaseLTI1p3Provider
from .base_lti_provider import BaseLTIProvider
from .base_notification import BaseNotification
from .base_release_info import BaseReleaseInfo
from .base_rubric_item import BaseRubricItem
from .base_tenant_coupon import BaseTenantCoupon
from .blackboard_zip_upload_enabled_setting import (
    BlackboardZipUploadEnabledSetting,
)
from .bulk_enroll_course_data import BulkEnrollCourseData
from .canvas_course_id_copying_enabled_setting import (
    CanvasCourseIdCopyingEnabledSetting,
)
from .cg_ignore_version import CGIgnoreVersion
from .change_user_role_course_data import ChangeUserRoleCourseData
from .check_points_as_json import CheckPointsAsJSON
from .check_points_data import CheckPointsData
from .check_points_extra import CheckPointsExtra
from .check_points_input_as_json import CheckPointsInputAsJSON
from .clone_result import CloneResult
from .code_editor_output_viewer_title_setting import (
    CodeEditorOutputViewerTitleSetting,
)
from .code_editor_start_on_assignment_description_setting import (
    CodeEditorStartOnAssignmentDescriptionSetting,
)
from .code_quality_as_json import CodeQualityAsJSON
from .code_quality_base_data import CodeQualityBaseData
from .code_quality_data import CodeQualityData
from .code_quality_extra import CodeQualityExtra
from .code_quality_input_as_json import CodeQualityInputAsJSON
from .code_quality_penalties import CodeQualityPenalties
from .column_range import ColumnRange
from .comment_base import CommentBase
from .comment_reply import CommentReply
from .comment_reply_edit import CommentReplyEdit
from .comment_reply_type import CommentReplyType
from .comment_type import CommentType
from .community_library_publishing_setting import (
    CommunityLibraryPublishingSetting,
)
from .community_library_setting import CommunityLibrarySetting
from .connect_repository_git_provider_data import (
    ConnectRepositoryGitProviderData,
)
from .copy_auto_test_data import CopyAutoTestData
from .copy_rubric_assignment_data import CopyRubricAssignmentData
from .coupon_data_parser import CouponDataParser
from .coupon_with_code import CouponWithCode
from .coupon_without_code import CouponWithoutCode
from .course import Course
from .course_bulk_enroll_result import CourseBulkEnrollResult
from .course_bulk_register_enabled_setting import (
    CourseBulkRegisterEnabledSetting,
)
from .course_coupon import CourseCoupon
from .course_coupon_usage import CourseCouponUsage
from .course_gradebook_enabled_setting import CourseGradebookEnabledSetting
from .course_gradebook_render_warning_size_setting import (
    CourseGradebookRenderWarningSizeSetting,
)
from .course_of_course_price import CourseOfCoursePrice
from .course_of_tenant_coupon_usage import CourseOfTenantCouponUsage
from .course_perm_map import CoursePermMap
from .course_permission import CoursePermission
from .course_price import CoursePrice
from .course_register_enabled_setting import CourseRegisterEnabledSetting
from .course_registration_link import CourseRegistrationLink
from .course_role import CourseRole
from .course_role_as_json_with_perms import CourseRoleAsJSONWithPerms
from .course_section import CourseSection
from .course_section_division import CourseSectionDivision
from .course_section_division_connection import CourseSectionDivisionConnection
from .course_section_division_user import CourseSectionDivisionUser
from .course_snippet import CourseSnippet
from .course_state import CourseState
from .course_statistics_as_json import CourseStatisticsAsJSON
from .create_assignment_course_data import CreateAssignmentCourseData
from .create_auto_test_data import CreateAutoTestData
from .create_comment_data import CreateCommentData
from .create_comment_reply_data import CreateCommentReplyData
from .create_course_data import CreateCourseData
from .create_division_section_data import CreateDivisionSectionData
from .create_group_group_set_data import CreateGroupGroupSetData
from .create_group_set_course_data import CreateGroupSetCourseData
from .create_lti_data import CreateLTIData
from .create_output_html_proxy_auto_test_data import (
    CreateOutputHtmlProxyAutoTestData,
)
from .create_proxy_submission_data import CreateProxySubmissionData
from .create_repository_git_provider_data import (
    CreateRepositoryGitProviderData,
)
from .create_role_course_data import CreateRoleCourseData
from .create_section_course_data import CreateSectionCourseData
from .create_snippet_course_data import CreateSnippetCourseData
from .create_snippet_data import CreateSnippetData
from .create_sso_provider_data import CreateSSOProviderData
from .create_tenant_data import CreateTenantData
from .csv_large_file_limit_setting import CsvLargeFileLimitSetting
from .csv_too_many_errors_limit_setting import CsvTooManyErrorsLimitSetting
from .currency import Currency
from .custom_output_as_json import CustomOutputAsJSON
from .custom_output_data import CustomOutputData
from .custom_output_extra import CustomOutputExtra
from .custom_output_input_as_json import CustomOutputInputAsJSON
from .custom_output_log import CustomOutputLog
from .custom_output_log_base import CustomOutputLogBase
from .default_course_ta_role_setting import DefaultCourseTaRoleSetting
from .default_course_teacher_role_setting import (
    DefaultCourseTeacherRoleSetting,
)
from .default_submission_page_tab_setting import (
    DefaultSubmissionPageTabSetting,
)
from .deleted_comment_reply import DeletedCommentReply
from .deletion_type import DeletionType
from .directory_with_children import DirectoryWithChildren
from .disabled_setting_exception import DisabledSettingException
from .display_grades_enabled_setting import DisplayGradesEnabledSetting
from .editor_enabled_for_teachers_setting import (
    EditorEnabledForTeachersSetting,
)
from .editor_enabled_setting import EditorEnabledSetting
from .email_notification_types import EmailNotificationTypes
from .email_students_enabled_setting import EmailStudentsEnabledSetting
from .email_users_course_data import EmailUsersCourseData
from .exam_login_max_length_setting import ExamLoginMaxLengthSetting
from .export_assignment_csv_data import ExportAssignmentCSVData
from .export_assignment_data import ExportAssignmentData
from .export_assignment_files_data import ExportAssignmentFilesData
from .extended_auto_test_result import ExtendedAutoTestResult
from .extended_auto_test_run import ExtendedAutoTestRun
from .extended_course import ExtendedCourse
from .extended_course_registration_link import ExtendedCourseRegistrationLink
from .extended_course_section import ExtendedCourseSection
from .extended_group import ExtendedGroup
from .extended_job import ExtendedJob
from .extended_non_deleted_comment_reply import ExtendedNonDeletedCommentReply
from .extended_tenant import ExtendedTenant
from .extended_transaction import ExtendedTransaction
from .extended_user import ExtendedUser
from .extended_work import ExtendedWork
from .extract_file_tree_directory import ExtractFileTreeDirectory
from .extract_file_tree_file import ExtractFileTreeFile
from .failed_to_send_email_exception import FailedToSendEmailException
from .feedback_base import FeedbackBase
from .feedback_threads_initially_collapsed_setting import (
    FeedbackThreadsInitiallyCollapsedSetting,
)
from .feedback_with_replies import FeedbackWithReplies
from .feedback_without_replies import FeedbackWithoutReplies
from .file_deletion import FileDeletion
from .file_rule import FileRule
from .file_rule_input_data import FileRuleInputData
from .file_tree import FileTree
from .file_type import FileType
from .finalized_lti1p1_provider import FinalizedLTI1p1Provider
from .finalized_lti1p3_provider import FinalizedLTI1p3Provider
from .first_day_of_week_from_locale_setting import (
    FirstDayOfWeekFromLocaleSetting,
)
from .first_phase_lti_launch_exception import FirstPhaseLTILaunchException
from .fixed_availability import FixedAvailability
from .fixed_grade_availability import FixedGradeAvailability
from .fixture_like import FixtureLike
from .fraction import Fraction
from .frontend_site_settings import FrontendSiteSettings
from .general_feedback_comment_base import GeneralFeedbackCommentBase
from .general_feedback_comment_base_with_extended_replies import (
    GeneralFeedbackCommentBaseWithExtendedReplies,
)
from .general_feedback_extra import GeneralFeedbackExtra
from .git_repositories_page import GitRepositoriesPage
from .git_repository_like import GitRepositoryLike
from .git_user_info import GitUserInfo
from .github_template_repo_enabled_setting import (
    GithubTemplateRepoEnabledSetting,
)
from .global_perm_map import GlobalPermMap
from .global_permission import GlobalPermission
from .grade_history import GradeHistory
from .grade_origin import GradeOrigin
from .grading_notifications_enabled_setting import (
    GradingNotificationsEnabledSetting,
)
from .group import Group
from .group_not_ready_for_submission_exception import (
    GroupNotReadyForSubmissionException,
)
from .group_set import GroupSet
from .groups_enabled_setting import GroupsEnabledSetting
from .has_unread_notifcation_json import HasUnreadNotifcationJSON
from .health_information import HealthInformation
from .hide_code_editor_filetree_controls_with_only_quiz_steps_setting import (
    HideCodeEditorFiletreeControlsWithOnlyQuizStepsSetting,
)
from .hide_code_editor_output_viewer_with_only_quiz_steps_setting import (
    HideCodeEditorOutputViewerWithOnlyQuizStepsSetting,
)
from .hide_empty_rubric_row_description_setting import (
    HideEmptyRubricRowDescriptionSetting,
)
from .hide_no_deadline_enabled_setting import HideNoDeadlineEnabledSetting
from .hubspot_syncing_enabled_setting import HubspotSyncingEnabledSetting
from .ignore_handling import IgnoreHandling
from .ignored_files_exception import IgnoredFilesException
from .import_into_assignment_data import ImportIntoAssignmentData
from .import_into_course_data import ImportIntoCourseData
from .incremental_rubric_submission_enabled_setting import (
    IncrementalRubricSubmissionEnabledSetting,
)
from .inline_feedback_comment_base import InlineFeedbackCommentBase
from .inline_feedback_comment_base_with_extended_replies import (
    InlineFeedbackCommentBaseWithExtendedReplies,
)
from .inline_feedback_extra import InlineFeedbackExtra
from .inline_feedback_on_quizzes_enabled_setting import (
    InlineFeedbackOnQuizzesEnabledSetting,
)
from .inline_rubric_viewer_enabled_setting import (
    InlineRubricViewerEnabledSetting,
)
from .invalid_group_exception import InvalidGroupException
from .invalid_io_cases_exception import InvalidIOCasesException
from .invalid_options_exception import InvalidOptionsException
from .io_test_as_json import IOTestAsJSON
from .io_test_base_data import IOTestBaseData
from .io_test_data import IOTestData
from .io_test_extra import IOTestExtra
from .io_test_input_as_json import IOTestInputAsJSON
from .io_test_input_case import IOTestInputCase
from .io_test_log import IOTestLog
from .io_test_option import IOTestOption
from .io_test_step_log import IOTestStepLog
from .io_test_step_log_base import IOTestStepLogBase
from .is_admin_permission_enabled_setting import (
    IsAdminPermissionEnabledSetting,
)
from .is_pearson_setting import IsPearsonSetting
from .job import Job
from .json_create_auto_test import JsonCreateAutoTest
from .json_create_tenant import JsonCreateTenant
from .json_patch_auto_test import JsonPatchAutoTest
from .json_patch_submit_types_assignment import JsonPatchSubmitTypesAssignment
from .junit_test_as_json import JunitTestAsJSON
from .junit_test_base_data import JunitTestBaseData
from .junit_test_data import JunitTestData
from .junit_test_extra import JunitTestExtra
from .junit_test_input_as_json import JunitTestInputAsJSON
from .junit_test_log import JunitTestLog
from .junit_test_log_base import JunitTestLogBase
from .jupyter_notebook_editor_enabled_setting import (
    JupyterNotebookEditorEnabledSetting,
)
from .jupyter_notebook_running_enabled_setting import (
    JupyterNotebookRunningEnabledSetting,
)
from .jwt_access_token_expires_setting import JwtAccessTokenExpiresSetting
from .legacy_features import LegacyFeatures
from .line_range import LineRange
from .linters_enabled_setting import LintersEnabledSetting
from .lms_capabilities import LMSCapabilities
from .login_token_before_time_setting import LoginTokenBeforeTimeSetting
from .login_user_data import LoginUserData
from .logout_response import LogoutResponse
from .logout_user_data import LogoutUserData
from .lti1p1_provider import LTI1p1Provider
from .lti1p1_provider_data import LTI1p1ProviderData
from .lti1p3_nonce_and_state_validation_enabled_setting import (
    Lti1p3NonceAndStateValidationEnabledSetting,
)
from .lti1p3_parse_most_privileged_role_setting import (
    Lti1p3ParseMostPrivilegedRoleSetting,
)
from .lti1p3_prevent_nonce_reuse_enabled_setting import (
    Lti1p3PreventNonceReuseEnabledSetting,
)
from .lti1p3_provider import LTI1p3Provider
from .lti1p3_provider_data import LTI1p3ProviderData
from .lti1p3_provider_presentation_as_json import (
    LTI1p3ProviderPresentationAsJSON,
)
from .lti1p3_system_role_from_context_role_setting import (
    Lti1p3SystemRoleFromContextRoleSetting,
)
from .lti_enabled_setting import LtiEnabledSetting
from .lti_launch_data_logging_setting import LtiLaunchDataLoggingSetting
from .lti_lock_date_copying_enabled_setting import (
    LtiLockDateCopyingEnabledSetting,
)
from .lti_provider_base import LTIProviderBase
from .lti_unset_deadline_lock_date_enabled_setting import (
    LtiUnsetDeadlineLockDateEnabledSetting,
)
from .max_document_update_size_setting import MaxDocumentUpdateSizeSetting
from .max_dynamo_file_size_setting import MaxDynamoFileSizeSetting
from .max_dynamo_submission_size_setting import MaxDynamoSubmissionSizeSetting
from .max_file_size_setting import MaxFileSizeSetting
from .max_large_upload_size_setting import MaxLargeUploadSizeSetting
from .max_lines_setting import MaxLinesSetting
from .max_normal_upload_size_setting import MaxNormalUploadSizeSetting
from .max_number_of_files_setting import MaxNumberOfFilesSetting
from .max_plagiarism_matches_setting import MaxPlagiarismMatchesSetting
from .max_user_setting_amount_setting import MaxUserSettingAmountSetting
from .min_password_score_setting import MinPasswordScoreSetting
from .mirror_file_result import MirrorFileResult
from .missing_cookie_error import MissingCookieError
from .missing_file import MissingFile
from .name_and_email_from_nrps_only_setting import (
    NameAndEmailFromNrpsOnlySetting,
)
from .new_auto_test_allowed_initial_build_ids_setting import (
    NewAutoTestAllowedInitialBuildIdsSetting,
)
from .new_auto_test_build_max_command_time_setting import (
    NewAutoTestBuildMaxCommandTimeSetting,
)
from .new_auto_test_build_output_limit_setting import (
    NewAutoTestBuildOutputLimitSetting,
)
from .new_auto_test_copying_enabled_setting import (
    NewAutoTestCopyingEnabledSetting,
)
from .new_auto_test_current_initial_build_ids_setting import (
    NewAutoTestCurrentInitialBuildIdsSetting,
)
from .new_auto_test_diff_viewer_enabled_setting import (
    NewAutoTestDiffViewerEnabledSetting,
)
from .new_auto_test_enabled_setting import NewAutoTestEnabledSetting
from .new_auto_test_initial_build_id_setting import (
    NewAutoTestInitialBuildIdSetting,
)
from .new_auto_test_max_dynamodb_size_setting import (
    NewAutoTestMaxDynamodbSizeSetting,
)
from .new_auto_test_max_file_size_setting import NewAutoTestMaxFileSizeSetting
from .new_auto_test_max_output_files_size_setting import (
    NewAutoTestMaxOutputFilesSizeSetting,
)
from .new_auto_test_max_storage_size_setting import (
    NewAutoTestMaxStorageSizeSetting,
)
from .new_auto_test_old_submission_age_setting import (
    NewAutoTestOldSubmissionAgeSetting,
)
from .new_auto_test_test_max_command_time_setting import (
    NewAutoTestTestMaxCommandTimeSetting,
)
from .new_auto_test_test_output_limit_setting import (
    NewAutoTestTestOutputLimitSetting,
)
from .new_auto_test_uncollapsing_step_output_delay_setting import (
    NewAutoTestUncollapsingStepOutputDelaySetting,
)
from .no_permissions import NoPermissions
from .non_deleted_comment_reply import NonDeletedCommentReply
from .non_finalized_lti1p1_provider import NonFinalizedLTI1p1Provider
from .non_finalized_lti1p3_provider import NonFinalizedLTI1p3Provider
from .non_present_preference import NonPresentPreference
from .notification import Notification
from .notification_comment_reply_notification_as_json import (
    NotificationCommentReplyNotificationAsJSON,
)
from .notification_general_feedback_reply_notification_as_json import (
    NotificationGeneralFeedbackReplyNotificationAsJSON,
)
from .notification_poll_time_setting import NotificationPollTimeSetting
from .notification_reasons import NotificationReasons
from .notification_setting import NotificationSetting
from .notification_setting_option import NotificationSettingOption
from .notifications_json import NotificationsJSON
from .oauth_provider import OAuthProvider
from .oauth_token import OAuthToken
from .option import Option
from .options_input_data import OptionsInputData
from .output_viewer_animation_limit_lines_count_setting import (
    OutputViewerAnimationLimitLinesCountSetting,
)
from .output_viewer_auto_expand_failed_steps_setting import (
    OutputViewerAutoExpandFailedStepsSetting,
)
from .parse_api_exception import ParseAPIException
from .patch1_p1_provider_lti_data import Patch1P1ProviderLTIData
from .patch1_p3_provider_lti_data import Patch1P3ProviderLTIData
from .patch_all_notification_data import PatchAllNotificationData
from .patch_assignment_data import PatchAssignmentData
from .patch_auto_test_data import PatchAutoTestData
from .patch_comment_reply_data import PatchCommentReplyData
from .patch_course_data import PatchCourseData
from .patch_grader_submission_data import PatchGraderSubmissionData
from .patch_notification_data import PatchNotificationData
from .patch_notification_setting_user_setting_data import (
    PatchNotificationSettingUserSettingData,
)
from .patch_provider_lti_data import PatchProviderLTIData
from .patch_role_course_data import PatchRoleCourseData
from .patch_role_data import PatchRoleData
from .patch_role_tenant_data import PatchRoleTenantData
from .patch_rubric_category_type_assignment_data import (
    PatchRubricCategoryTypeAssignmentData,
)
from .patch_rubric_result_submission_data import (
    PatchRubricResultSubmissionData,
)
from .patch_section_data import PatchSectionData
from .patch_settings_tenant_data import PatchSettingsTenantData
from .patch_site_settings_data import PatchSiteSettingsData
from .patch_snippet_course_data import PatchSnippetCourseData
from .patch_snippet_data import PatchSnippetData
from .patch_submission_data import PatchSubmissionData
from .patch_submit_types_assignment_data import PatchSubmitTypesAssignmentData
from .patch_tenant_data import PatchTenantData
from .patch_ui_preference_user_setting_data import (
    PatchUiPreferenceUserSettingData,
)
from .patch_user_data import PatchUserData
from .pay_with_coupon_course_price_data import PayWithCouponCoursePriceData
from .pearson_templates_setting import PearsonTemplatesSetting
from .pearson_try_out_coding_question_enabled_setting import (
    PearsonTryOutCodingQuestionEnabledSetting,
)
from .peer_feedback_enabled_setting import PeerFeedbackEnabledSetting
from .permission_exception import PermissionException
from .plagiarism_bulk_export_enabled_setting import (
    PlagiarismBulkExportEnabledSetting,
)
from .plagiarism_bulk_export_max_cases_setting import (
    PlagiarismBulkExportMaxCasesSetting,
)
from .plagiarism_case import PlagiarismCase
from .plagiarism_pdf_export_enabled_setting import (
    PlagiarismPdfExportEnabledSetting,
)
from .plagiarism_run import PlagiarismRun
from .plagiarism_run_plagiarism_assignment_as_json import (
    PlagiarismRunPlagiarismAssignmentAsJSON,
)
from .plagiarism_run_plagiarism_course_as_json import (
    PlagiarismRunPlagiarismCourseAsJSON,
)
from .plagiarism_state import PlagiarismState
from .post_oauth_token_data import PostOAuthTokenData
from .present_preference import PresentPreference
from .prompt_engineering_step_enabled_setting import (
    PromptEngineeringStepEnabledSetting,
)
from .proxy import Proxy
from .put_description_assignment_data import PutDescriptionAssignmentData
from .put_enroll_link_course_data import PutEnrollLinkCourseData
from .put_price_course_data import PutPriceCourseData
from .put_price_tenant_data import PutPriceTenantData
from .put_rubric_assignment_data import PutRubricAssignmentData
from .quality_comment_severity import QualityCommentSeverity
from .quality_comments_in_code_editor_setting import (
    QualityCommentsInCodeEditorSetting,
)
from .quality_test_log import QualityTestLog
from .quality_test_log_base import QualityTestLogBase
from .quiz_single_question_mode_hide_run_button_enabled_setting import (
    QuizSingleQuestionModeHideRunButtonEnabledSetting,
)
from .register_enabled_setting import RegisterEnabledSetting
from .register_user_data import RegisterUserData
from .register_user_with_link_course_data import RegisterUserWithLinkCourseData
from .release_info import ReleaseInfo
from .release_message_max_time_setting import ReleaseMessageMaxTimeSetting
from .removed_permissions import RemovedPermissions
from .rename_group_group_data import RenameGroupGroupData
from .render_html_enabled_setting import RenderHtmlEnabledSetting
from .repository_connection_limit_reached_exception import (
    RepositoryConnectionLimitReachedException,
)
from .reset_token_time_setting import ResetTokenTimeSetting
from .result_data_get_auto_test_get import ResultDataGetAutoTestGet
from .result_data_get_task_result_get_all import ResultDataGetTaskResultGetAll
from .result_data_post_section_create_division import (
    ResultDataPostSectionCreateDivision,
)
from .retry_group_submission_grade_passback_enabled_setting import (
    RetryGroupSubmissionGradePassbackEnabledSetting,
)
from .role_as_json_with_perms import RoleAsJSONWithPerms
from .root_file_trees_json import RootFileTreesJSON
from .rubric_description_type import RubricDescriptionType
from .rubric_enabled_for_teacher_on_submissions_page_setting import (
    RubricEnabledForTeacherOnSubmissionsPageSetting,
)
from .rubric_item import RubricItem
from .rubric_item_input_as_json import RubricItemInputAsJSON
from .rubric_lock_reason import RubricLockReason
from .rubric_row_base import RubricRowBase
from .rubric_row_base_input_as_json import RubricRowBaseInputAsJSON
from .rubric_row_base_input_base_as_json import RubricRowBaseInputBaseAsJSON
from .rubrics_enabled_setting import RubricsEnabledSetting
from .rule_type import RuleType
from .run_program_as_json import RunProgramAsJSON
from .run_program_data import RunProgramData
from .run_program_extra import RunProgramExtra
from .run_program_input_as_json import RunProgramInputAsJSON
from .run_program_log import RunProgramLog
from .saml2_provider_json import Saml2ProviderJSON
from .saml_ui_info import SamlUiInfo
from .sections_in_submission_list_enabled_setting import (
    SectionsInSubmissionListEnabledSetting,
)
from .send_registration_email_setting import SendRegistrationEmailSetting
from .server_time_correction_enabled_setting import (
    ServerTimeCorrectionEnabledSetting,
)
from .server_time_diff_tolerance_setting import ServerTimeDiffToleranceSetting
from .server_time_sync_interval_setting import ServerTimeSyncIntervalSetting
from .session_restriction_context import SessionRestrictionContext
from .session_restriction_data import SessionRestrictionData
from .setting_token_time_setting import SettingTokenTimeSetting
from .setup_oauth_result import SetupOAuthResult
from .simple_submission_mode_enabled_setting import (
    SimpleSubmissionModeEnabledSetting,
)
from .simple_submission_navigate_to_latest_editor_session_setting import (
    SimpleSubmissionNavigateToLatestEditorSessionSetting,
)
from .site_email_setting import SiteEmailSetting
from .site_setting_input import SiteSettingInput
from .snippet import Snippet
from .sso_infer_global_staff_role_setting import SsoInferGlobalStaffRoleSetting
from .sso_username_decollision_enabled_setting import (
    SsoUsernameDecollisionEnabledSetting,
)
from .staged_assignment_importer_enabled_setting import (
    StagedAssignmentImporterEnabledSetting,
)
from .start_payment_course_price_close_tab_data import (
    StartPaymentCoursePriceCloseTabData,
)
from .start_payment_course_price_data import StartPaymentCoursePriceData
from .start_payment_course_price_redirect_data import (
    StartPaymentCoursePriceRedirectData,
)
from .started_transaction import StartedTransaction
from .student_payment_enabled_setting import StudentPaymentEnabledSetting
from .student_payment_main_option_setting import (
    StudentPaymentMainOptionSetting,
)
from .student_view_enabled_setting import StudentViewEnabledSetting
from .submission_validator_input_data import SubmissionValidatorInputData
from .submissions_per_page_enabled_setting import (
    SubmissionsPerPageEnabledSetting,
)
from .task_result_state import TaskResultState
from .tax_behavior import TaxBehavior
from .tenant import Tenant
from .tenant_coupon import TenantCoupon
from .tenant_coupon_usage import TenantCouponUsage
from .tenant_coupon_with_code import TenantCouponWithCode
from .tenant_coupon_without_code import TenantCouponWithoutCode
from .tenant_course_statistics import TenantCourseStatistics
from .tenant_of_tenant_price import TenantOfTenantPrice
from .tenant_permissions import TenantPermissions
from .tenant_price import TenantPrice
from .tenant_role_as_json_with_perms import TenantRoleAsJSONWithPerms
from .tenant_statistics import TenantStatistics
from .test_submission_copying_on_import_enabled_setting import (
    TestSubmissionCopyingOnImportEnabledSetting,
)
from .timed_availability import TimedAvailability
from .timeframe_like import TimeframeLike
from .token_revoked_exception import TokenRevokedException
from .transaction import Transaction
from .transaction_state import TransactionState
from .types import *
from .update_peer_feedback_settings_assignment_data import (
    UpdatePeerFeedbackSettingsAssignmentData,
)
from .update_set_auto_test_data import UpdateSetAutoTestData
from .update_suite_auto_test_base_data import UpdateSuiteAutoTestBaseData
from .update_suite_auto_test_data import UpdateSuiteAutoTestData
from .upgraded_lti_provider_exception import UpgradedLTIProviderException
from .upload_submission_assignment_data import UploadSubmissionAssignmentData
from .user import User
from .user_course import UserCourse
from .user_info_with_role import UserInfoWithRole
from .user_input import UserInput
from .user_login_response import UserLoginResponse
from .user_without_group import UserWithoutGroup
from .warning_for_missing_newline_enabled_setting import (
    WarningForMissingNewlineEnabledSetting,
)
from .weak_password_exception import WeakPasswordException
from .weak_password_feedback import WeakPasswordFeedback
from .webhook_base import WebhookBase
from .webhook_configuration_disabled_as_json import (
    WebhookConfigurationDisabledAsJSON,
)
from .webhook_configuration_enabled_as_json import (
    WebhookConfigurationEnabledAsJSON,
)
from .work import Work
from .work_origin import WorkOrigin
from .work_rubric_item import WorkRubricItem
from .work_rubric_result_as_json import WorkRubricResultAsJSON
from .work_rubric_result_points_as_json import WorkRubricResultPointsAsJSON
