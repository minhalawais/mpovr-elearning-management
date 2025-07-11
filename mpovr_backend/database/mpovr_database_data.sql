PGDMP                       |            mpovr    17.2    17.2 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    24576    mpovr    DATABASE     �   CREATE DATABASE mpovr WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE mpovr;
                     postgres    false            �           0    0    SCHEMA public    ACL     *   GRANT ALL ON SCHEMA public TO role_admin;
                        pg_database_owner    false    5            t           1247    24588    application_status    TYPE     a   CREATE TYPE public.application_status AS ENUM (
    'pending',
    'approved',
    'rejected'
);
 %   DROP TYPE public.application_status;
       public               postgres    false            }           1247    24612    content_type    TYPE     �   CREATE TYPE public.content_type AS ENUM (
    'virtual_live_session',
    'video',
    'reading',
    'assignment',
    'practicum',
    'presentation',
    'quiz'
);
    DROP TYPE public.content_type;
       public               postgres    false            �           1247    24628    enrollment_status    TYPE     d   CREATE TYPE public.enrollment_status AS ENUM (
    'active',
    'completed',
    'discontinued'
);
 $   DROP TYPE public.enrollment_status;
       public               postgres    false            z           1247    24604    message_status    TYPE     ]   CREATE TYPE public.message_status AS ENUM (
    'pending',
    'approved',
    'rejected'
);
 !   DROP TYPE public.message_status;
       public               postgres    false            w           1247    24596    payment_status    TYPE     ^   CREATE TYPE public.payment_status AS ENUM (
    'pending',
    'completed',
    'refunded'
);
 !   DROP TYPE public.payment_status;
       public               postgres    false            q           1247    24578 	   user_role    TYPE     f   CREATE TYPE public.user_role AS ENUM (
    'learner',
    'trainer',
    'admin',
    'role_admin'
);
    DROP TYPE public.user_role;
       public               postgres    false            �            1259    24909 
   agreements    TABLE     t  CREATE TABLE public.agreements (
    agreement_id integer NOT NULL,
    user_id integer,
    program_id integer,
    agreement_text text NOT NULL,
    signed_at timestamp with time zone,
    docusign_envelope_id character varying(100),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.agreements;
       public         heap r       postgres    false            �           0    0    TABLE agreements    ACL     �   GRANT SELECT ON TABLE public.agreements TO learner;
GRANT ALL ON TABLE public.agreements TO admin;
GRANT ALL ON TABLE public.agreements TO role_admin;
          public               postgres    false    250            �            1259    24908    agreements_agreement_id_seq    SEQUENCE     �   CREATE SEQUENCE public.agreements_agreement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.agreements_agreement_id_seq;
       public               postgres    false    250            �           0    0    agreements_agreement_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.agreements_agreement_id_seq OWNED BY public.agreements.agreement_id;
          public               postgres    false    249            �            1259    24678    applications    TABLE     �  CREATE TABLE public.applications (
    application_id integer NOT NULL,
    user_id integer,
    program_id integer,
    status public.application_status DEFAULT 'pending'::public.application_status NOT NULL,
    interview_slot timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
     DROP TABLE public.applications;
       public         heap r       postgres    false    884    884            �           0    0    TABLE applications    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.applications TO learner;
GRANT ALL ON TABLE public.applications TO admin;
GRANT ALL ON TABLE public.applications TO role_admin;
          public               postgres    false    224            �            1259    24677    applications_application_id_seq    SEQUENCE     �   CREATE SEQUENCE public.applications_application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.applications_application_id_seq;
       public               postgres    false    224            �           0    0    applications_application_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.applications_application_id_seq OWNED BY public.applications.application_id;
          public               postgres    false    223            �            1259    24770    assignments    TABLE     #  CREATE TABLE public.assignments (
    assignment_id integer NOT NULL,
    content_id integer,
    description text,
    due_date timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.assignments;
       public         heap r       postgres    false            �           0    0    TABLE assignments    ACL     �   GRANT SELECT ON TABLE public.assignments TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.assignments TO trainer;
GRANT ALL ON TABLE public.assignments TO admin;
GRANT ALL ON TABLE public.assignments TO role_admin;
          public               postgres    false    234            �            1259    24769    assignments_assignment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.assignments_assignment_id_seq;
       public               postgres    false    234            �           0    0    assignments_assignment_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.assignments_assignment_id_seq OWNED BY public.assignments.assignment_id;
          public               postgres    false    233            �            1259    24754    content    TABLE     !  CREATE TABLE public.content (
    content_id integer NOT NULL,
    module_id integer,
    title character varying(255) NOT NULL,
    content_type public.content_type NOT NULL,
    content_url character varying(255),
    content_text text,
    file_path character varying(255),
    order_number integer NOT NULL,
    opens_at timestamp with time zone NOT NULL,
    closes_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.content;
       public         heap r       postgres    false    893            �           0    0    TABLE content    ACL     �   GRANT SELECT ON TABLE public.content TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.content TO trainer;
GRANT ALL ON TABLE public.content TO admin;
GRANT ALL ON TABLE public.content TO role_admin;
          public               postgres    false    232            �            1259    24753    content_content_id_seq    SEQUENCE     �   CREATE SEQUENCE public.content_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.content_content_id_seq;
       public               postgres    false    232            �           0    0    content_content_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.content_content_id_seq OWNED BY public.content.content_id;
          public               postgres    false    231            �            1259    24718    enrollments    TABLE     �  CREATE TABLE public.enrollments (
    enrollment_id integer NOT NULL,
    user_id integer,
    program_id integer,
    start_date date NOT NULL,
    end_date date,
    status public.enrollment_status DEFAULT 'active'::public.enrollment_status NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.enrollments;
       public         heap r       postgres    false    896    896            �           0    0    TABLE enrollments    ACL     �   GRANT SELECT ON TABLE public.enrollments TO learner;
GRANT SELECT ON TABLE public.enrollments TO trainer;
GRANT ALL ON TABLE public.enrollments TO admin;
GRANT ALL ON TABLE public.enrollments TO role_admin;
          public               postgres    false    228            �            1259    24717    enrollments_enrollment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.enrollments_enrollment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.enrollments_enrollment_id_seq;
       public               postgres    false    228            �           0    0    enrollments_enrollment_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.enrollments_enrollment_id_seq OWNED BY public.enrollments.enrollment_id;
          public               postgres    false    227            �            1259    24887    messages    TABLE     h  CREATE TABLE public.messages (
    message_id integer NOT NULL,
    sender_id integer,
    recipient_id integer,
    content text NOT NULL,
    status public.message_status DEFAULT 'pending'::public.message_status NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.messages;
       public         heap r       postgres    false    890    890            �           0    0    TABLE messages    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.messages TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.messages TO trainer;
GRANT ALL ON TABLE public.messages TO admin;
GRANT ALL ON TABLE public.messages TO role_admin;
          public               postgres    false    248            �            1259    24886    messages_message_id_seq    SEQUENCE     �   CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.messages_message_id_seq;
       public               postgres    false    248            �           0    0    messages_message_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;
          public               postgres    false    247            �            1259    24738    modules    TABLE     A  CREATE TABLE public.modules (
    module_id integer NOT NULL,
    program_id integer,
    name character varying(100) NOT NULL,
    description text,
    order_number integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.modules;
       public         heap r       postgres    false            �           0    0    TABLE modules    ACL     �   GRANT SELECT ON TABLE public.modules TO learner;
GRANT SELECT ON TABLE public.modules TO trainer;
GRANT ALL ON TABLE public.modules TO admin;
GRANT ALL ON TABLE public.modules TO role_admin;
          public               postgres    false    230            �            1259    24737    modules_module_id_seq    SEQUENCE     �   CREATE SEQUENCE public.modules_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.modules_module_id_seq;
       public               postgres    false    230            �           0    0    modules_module_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.modules_module_id_seq OWNED BY public.modules.module_id;
          public               postgres    false    229            �            1259    24698    payments    TABLE     �  CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    user_id integer,
    program_id integer,
    amount numeric(10,2) NOT NULL,
    status public.payment_status DEFAULT 'pending'::public.payment_status NOT NULL,
    stripe_payment_id character varying(100),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.payments;
       public         heap r       postgres    false    887    887            �           0    0    TABLE payments    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.payments TO learner;
GRANT ALL ON TABLE public.payments TO admin;
GRANT ALL ON TABLE public.payments TO role_admin;
          public               postgres    false    226            �            1259    24697    payments_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.payments_payment_id_seq;
       public               postgres    false    226            �           0    0    payments_payment_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;
          public               postgres    false    225            �            1259    24651    profiles    TABLE     �  CREATE TABLE public.profiles (
    profile_id integer NOT NULL,
    user_id integer,
    full_name character varying(100) NOT NULL,
    date_of_birth date,
    phone_number character varying(20),
    address text,
    education_history jsonb,
    work_experience jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.profiles;
       public         heap r       postgres    false            �           0    0    TABLE profiles    ACL     �   GRANT SELECT ON TABLE public.profiles TO learner;
GRANT SELECT ON TABLE public.profiles TO trainer;
GRANT ALL ON TABLE public.profiles TO admin;
GRANT ALL ON TABLE public.profiles TO role_admin;
          public               postgres    false    220            �            1259    24650    profiles_profile_id_seq    SEQUENCE     �   CREATE SEQUENCE public.profiles_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.profiles_profile_id_seq;
       public               postgres    false    220            �           0    0    profiles_profile_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.profiles_profile_id_seq OWNED BY public.profiles.profile_id;
          public               postgres    false    219            �            1259    24667    programs    TABLE     >  CREATE TABLE public.programs (
    program_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    duration integer,
    fee numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.programs;
       public         heap r       postgres    false            �           0    0    TABLE programs    ACL     �   GRANT SELECT ON TABLE public.programs TO learner;
GRANT SELECT ON TABLE public.programs TO trainer;
GRANT ALL ON TABLE public.programs TO admin;
GRANT ALL ON TABLE public.programs TO role_admin;
          public               postgres    false    222            �            1259    24666    programs_program_id_seq    SEQUENCE     �   CREATE SEQUENCE public.programs_program_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.programs_program_id_seq;
       public               postgres    false    222            �           0    0    programs_program_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.programs_program_id_seq OWNED BY public.programs.program_id;
          public               postgres    false    221            �            1259    24930    progress_tracking    TABLE     *  CREATE TABLE public.progress_tracking (
    progress_id integer NOT NULL,
    user_id integer,
    content_id integer,
    completed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
 %   DROP TABLE public.progress_tracking;
       public         heap r       postgres    false            �           0    0    TABLE progress_tracking    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.progress_tracking TO learner;
GRANT SELECT,UPDATE ON TABLE public.progress_tracking TO trainer;
GRANT ALL ON TABLE public.progress_tracking TO admin;
GRANT ALL ON TABLE public.progress_tracking TO role_admin;
          public               postgres    false    252            �            1259    24929 !   progress_tracking_progress_id_seq    SEQUENCE     �   CREATE SEQUENCE public.progress_tracking_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.progress_tracking_progress_id_seq;
       public               postgres    false    252            �           0    0 !   progress_tracking_progress_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.progress_tracking_progress_id_seq OWNED BY public.progress_tracking.progress_id;
          public               postgres    false    251            �            1259    24848    quiz_attempts    TABLE     �   CREATE TABLE public.quiz_attempts (
    attempt_id integer NOT NULL,
    quiz_id integer,
    user_id integer,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone,
    score numeric(5,2)
);
 !   DROP TABLE public.quiz_attempts;
       public         heap r       postgres    false            �           0    0    TABLE quiz_attempts    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.quiz_attempts TO learner;
GRANT SELECT,UPDATE ON TABLE public.quiz_attempts TO trainer;
GRANT ALL ON TABLE public.quiz_attempts TO admin;
GRANT ALL ON TABLE public.quiz_attempts TO role_admin;
          public               postgres    false    244            �            1259    24847    quiz_attempts_attempt_id_seq    SEQUENCE     �   CREATE SEQUENCE public.quiz_attempts_attempt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.quiz_attempts_attempt_id_seq;
       public               postgres    false    244            �           0    0    quiz_attempts_attempt_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.quiz_attempts_attempt_id_seq OWNED BY public.quiz_attempts.attempt_id;
          public               postgres    false    243            �            1259    24834    quiz_options    TABLE     �   CREATE TABLE public.quiz_options (
    option_id integer NOT NULL,
    question_id integer,
    option_text text NOT NULL,
    is_correct boolean NOT NULL,
    order_number integer NOT NULL
);
     DROP TABLE public.quiz_options;
       public         heap r       postgres    false            �           0    0    TABLE quiz_options    ACL     �   GRANT SELECT ON TABLE public.quiz_options TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.quiz_options TO trainer;
GRANT ALL ON TABLE public.quiz_options TO admin;
GRANT ALL ON TABLE public.quiz_options TO role_admin;
          public               postgres    false    242            �            1259    24833    quiz_options_option_id_seq    SEQUENCE     �   CREATE SEQUENCE public.quiz_options_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.quiz_options_option_id_seq;
       public               postgres    false    242            �           0    0    quiz_options_option_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.quiz_options_option_id_seq OWNED BY public.quiz_options.option_id;
          public               postgres    false    241            �            1259    24820    quiz_questions    TABLE     �   CREATE TABLE public.quiz_questions (
    question_id integer NOT NULL,
    quiz_id integer,
    question_text text NOT NULL,
    question_type character varying(50) NOT NULL,
    order_number integer NOT NULL
);
 "   DROP TABLE public.quiz_questions;
       public         heap r       postgres    false            �           0    0    TABLE quiz_questions    ACL     �   GRANT SELECT ON TABLE public.quiz_questions TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.quiz_questions TO trainer;
GRANT ALL ON TABLE public.quiz_questions TO admin;
GRANT ALL ON TABLE public.quiz_questions TO role_admin;
          public               postgres    false    240            �            1259    24819    quiz_questions_question_id_seq    SEQUENCE     �   CREATE SEQUENCE public.quiz_questions_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.quiz_questions_question_id_seq;
       public               postgres    false    240            �           0    0    quiz_questions_question_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.quiz_questions_question_id_seq OWNED BY public.quiz_questions.question_id;
          public               postgres    false    239            �            1259    24865    quiz_responses    TABLE     �   CREATE TABLE public.quiz_responses (
    response_id integer NOT NULL,
    attempt_id integer,
    question_id integer,
    option_id integer
);
 "   DROP TABLE public.quiz_responses;
       public         heap r       postgres    false            �           0    0    TABLE quiz_responses    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.quiz_responses TO learner;
GRANT SELECT ON TABLE public.quiz_responses TO trainer;
GRANT ALL ON TABLE public.quiz_responses TO admin;
GRANT ALL ON TABLE public.quiz_responses TO role_admin;
          public               postgres    false    246            �            1259    24864    quiz_responses_response_id_seq    SEQUENCE     �   CREATE SEQUENCE public.quiz_responses_response_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.quiz_responses_response_id_seq;
       public               postgres    false    246            �           0    0    quiz_responses_response_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.quiz_responses_response_id_seq OWNED BY public.quiz_responses.response_id;
          public               postgres    false    245            �            1259    24804    quizzes    TABLE     5  CREATE TABLE public.quizzes (
    quiz_id integer NOT NULL,
    content_id integer,
    title character varying(255) NOT NULL,
    description text,
    time_limit integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.quizzes;
       public         heap r       postgres    false            �           0    0    TABLE quizzes    ACL     �   GRANT SELECT ON TABLE public.quizzes TO learner;
GRANT SELECT,INSERT,UPDATE ON TABLE public.quizzes TO trainer;
GRANT ALL ON TABLE public.quizzes TO admin;
GRANT ALL ON TABLE public.quizzes TO role_admin;
          public               postgres    false    238            �            1259    24803    quizzes_quiz_id_seq    SEQUENCE     �   CREATE SEQUENCE public.quizzes_quiz_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.quizzes_quiz_id_seq;
       public               postgres    false    238            �           0    0    quizzes_quiz_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.quizzes_quiz_id_seq OWNED BY public.quizzes.quiz_id;
          public               postgres    false    237            �            1259    24786    submissions    TABLE     �   CREATE TABLE public.submissions (
    submission_id integer NOT NULL,
    assignment_id integer,
    user_id integer,
    file_path character varying(255),
    submitted_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    grade numeric(5,2)
);
    DROP TABLE public.submissions;
       public         heap r       postgres    false            �           0    0    TABLE submissions    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.submissions TO learner;
GRANT SELECT,UPDATE ON TABLE public.submissions TO trainer;
GRANT ALL ON TABLE public.submissions TO admin;
GRANT ALL ON TABLE public.submissions TO role_admin;
          public               postgres    false    236            �            1259    24785    submissions_submission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.submissions_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.submissions_submission_id_seq;
       public               postgres    false    236            �           0    0    submissions_submission_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.submissions_submission_id_seq OWNED BY public.submissions.submission_id;
          public               postgres    false    235            �            1259    24636    users    TABLE     �  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role public.user_role NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    last_login timestamp with time zone,
    last_login_ip inet,
    two_factor_enabled boolean DEFAULT false,
    two_factor_secret character varying(255)
);
    DROP TABLE public.users;
       public         heap r       postgres    false    881            �           0    0    TABLE users    ACL     �   GRANT SELECT ON TABLE public.users TO learner;
GRANT SELECT ON TABLE public.users TO trainer;
GRANT ALL ON TABLE public.users TO admin;
GRANT ALL ON TABLE public.users TO role_admin;
          public               postgres    false    218            �            1259    24635    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    218            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    217            �           2604    24912    agreements agreement_id    DEFAULT     �   ALTER TABLE ONLY public.agreements ALTER COLUMN agreement_id SET DEFAULT nextval('public.agreements_agreement_id_seq'::regclass);
 F   ALTER TABLE public.agreements ALTER COLUMN agreement_id DROP DEFAULT;
       public               postgres    false    249    250    250            �           2604    24681    applications application_id    DEFAULT     �   ALTER TABLE ONLY public.applications ALTER COLUMN application_id SET DEFAULT nextval('public.applications_application_id_seq'::regclass);
 J   ALTER TABLE public.applications ALTER COLUMN application_id DROP DEFAULT;
       public               postgres    false    223    224    224            �           2604    24773    assignments assignment_id    DEFAULT     �   ALTER TABLE ONLY public.assignments ALTER COLUMN assignment_id SET DEFAULT nextval('public.assignments_assignment_id_seq'::regclass);
 H   ALTER TABLE public.assignments ALTER COLUMN assignment_id DROP DEFAULT;
       public               postgres    false    233    234    234            �           2604    24757    content content_id    DEFAULT     x   ALTER TABLE ONLY public.content ALTER COLUMN content_id SET DEFAULT nextval('public.content_content_id_seq'::regclass);
 A   ALTER TABLE public.content ALTER COLUMN content_id DROP DEFAULT;
       public               postgres    false    232    231    232            �           2604    24721    enrollments enrollment_id    DEFAULT     �   ALTER TABLE ONLY public.enrollments ALTER COLUMN enrollment_id SET DEFAULT nextval('public.enrollments_enrollment_id_seq'::regclass);
 H   ALTER TABLE public.enrollments ALTER COLUMN enrollment_id DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    24890    messages message_id    DEFAULT     z   ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);
 B   ALTER TABLE public.messages ALTER COLUMN message_id DROP DEFAULT;
       public               postgres    false    247    248    248            �           2604    24741    modules module_id    DEFAULT     v   ALTER TABLE ONLY public.modules ALTER COLUMN module_id SET DEFAULT nextval('public.modules_module_id_seq'::regclass);
 @   ALTER TABLE public.modules ALTER COLUMN module_id DROP DEFAULT;
       public               postgres    false    230    229    230            �           2604    24701    payments payment_id    DEFAULT     z   ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);
 B   ALTER TABLE public.payments ALTER COLUMN payment_id DROP DEFAULT;
       public               postgres    false    226    225    226            �           2604    24654    profiles profile_id    DEFAULT     z   ALTER TABLE ONLY public.profiles ALTER COLUMN profile_id SET DEFAULT nextval('public.profiles_profile_id_seq'::regclass);
 B   ALTER TABLE public.profiles ALTER COLUMN profile_id DROP DEFAULT;
       public               postgres    false    219    220    220            �           2604    24670    programs program_id    DEFAULT     z   ALTER TABLE ONLY public.programs ALTER COLUMN program_id SET DEFAULT nextval('public.programs_program_id_seq'::regclass);
 B   ALTER TABLE public.programs ALTER COLUMN program_id DROP DEFAULT;
       public               postgres    false    221    222    222            �           2604    24933    progress_tracking progress_id    DEFAULT     �   ALTER TABLE ONLY public.progress_tracking ALTER COLUMN progress_id SET DEFAULT nextval('public.progress_tracking_progress_id_seq'::regclass);
 L   ALTER TABLE public.progress_tracking ALTER COLUMN progress_id DROP DEFAULT;
       public               postgres    false    252    251    252            �           2604    24851    quiz_attempts attempt_id    DEFAULT     �   ALTER TABLE ONLY public.quiz_attempts ALTER COLUMN attempt_id SET DEFAULT nextval('public.quiz_attempts_attempt_id_seq'::regclass);
 G   ALTER TABLE public.quiz_attempts ALTER COLUMN attempt_id DROP DEFAULT;
       public               postgres    false    243    244    244            �           2604    24837    quiz_options option_id    DEFAULT     �   ALTER TABLE ONLY public.quiz_options ALTER COLUMN option_id SET DEFAULT nextval('public.quiz_options_option_id_seq'::regclass);
 E   ALTER TABLE public.quiz_options ALTER COLUMN option_id DROP DEFAULT;
       public               postgres    false    241    242    242            �           2604    24823    quiz_questions question_id    DEFAULT     �   ALTER TABLE ONLY public.quiz_questions ALTER COLUMN question_id SET DEFAULT nextval('public.quiz_questions_question_id_seq'::regclass);
 I   ALTER TABLE public.quiz_questions ALTER COLUMN question_id DROP DEFAULT;
       public               postgres    false    239    240    240            �           2604    24868    quiz_responses response_id    DEFAULT     �   ALTER TABLE ONLY public.quiz_responses ALTER COLUMN response_id SET DEFAULT nextval('public.quiz_responses_response_id_seq'::regclass);
 I   ALTER TABLE public.quiz_responses ALTER COLUMN response_id DROP DEFAULT;
       public               postgres    false    246    245    246            �           2604    24807    quizzes quiz_id    DEFAULT     r   ALTER TABLE ONLY public.quizzes ALTER COLUMN quiz_id SET DEFAULT nextval('public.quizzes_quiz_id_seq'::regclass);
 >   ALTER TABLE public.quizzes ALTER COLUMN quiz_id DROP DEFAULT;
       public               postgres    false    238    237    238            �           2604    24789    submissions submission_id    DEFAULT     �   ALTER TABLE ONLY public.submissions ALTER COLUMN submission_id SET DEFAULT nextval('public.submissions_submission_id_seq'::regclass);
 H   ALTER TABLE public.submissions ALTER COLUMN submission_id DROP DEFAULT;
       public               postgres    false    236    235    236            �           2604    24639    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    218    217    218            �          0    24909 
   agreements 
   TABLE DATA           �   COPY public.agreements (agreement_id, user_id, program_id, agreement_text, signed_at, docusign_envelope_id, created_at, updated_at) FROM stdin;
    public               postgres    false    250   ��       �          0    24678    applications 
   TABLE DATA           {   COPY public.applications (application_id, user_id, program_id, status, interview_slot, created_at, updated_at) FROM stdin;
    public               postgres    false    224   ��       �          0    24770    assignments 
   TABLE DATA           o   COPY public.assignments (assignment_id, content_id, description, due_date, created_at, updated_at) FROM stdin;
    public               postgres    false    234   �       �          0    24754    content 
   TABLE DATA           �   COPY public.content (content_id, module_id, title, content_type, content_url, content_text, file_path, order_number, opens_at, closes_at, created_at, updated_at) FROM stdin;
    public               postgres    false    232    �       �          0    24718    enrollments 
   TABLE DATA              COPY public.enrollments (enrollment_id, user_id, program_id, start_date, end_date, status, created_at, updated_at) FROM stdin;
    public               postgres    false    228   =�       �          0    24887    messages 
   TABLE DATA           p   COPY public.messages (message_id, sender_id, recipient_id, content, status, created_at, updated_at) FROM stdin;
    public               postgres    false    248   Z�       �          0    24738    modules 
   TABLE DATA           q   COPY public.modules (module_id, program_id, name, description, order_number, created_at, updated_at) FROM stdin;
    public               postgres    false    230   w�       �          0    24698    payments 
   TABLE DATA           ~   COPY public.payments (payment_id, user_id, program_id, amount, status, stripe_payment_id, created_at, updated_at) FROM stdin;
    public               postgres    false    226   ��       �          0    24651    profiles 
   TABLE DATA           �   COPY public.profiles (profile_id, user_id, full_name, date_of_birth, phone_number, address, education_history, work_experience, created_at, updated_at) FROM stdin;
    public               postgres    false    220   ��       �          0    24667    programs 
   TABLE DATA           h   COPY public.programs (program_id, name, description, duration, fee, created_at, updated_at) FROM stdin;
    public               postgres    false    222   ��       �          0    24930    progress_tracking 
   TABLE DATA           s   COPY public.progress_tracking (progress_id, user_id, content_id, completed_at, created_at, updated_at) FROM stdin;
    public               postgres    false    252   ��       �          0    24848    quiz_attempts 
   TABLE DATA           b   COPY public.quiz_attempts (attempt_id, quiz_id, user_id, start_time, end_time, score) FROM stdin;
    public               postgres    false    244   �       �          0    24834    quiz_options 
   TABLE DATA           e   COPY public.quiz_options (option_id, question_id, option_text, is_correct, order_number) FROM stdin;
    public               postgres    false    242   %�       �          0    24820    quiz_questions 
   TABLE DATA           j   COPY public.quiz_questions (question_id, quiz_id, question_text, question_type, order_number) FROM stdin;
    public               postgres    false    240   B�       �          0    24865    quiz_responses 
   TABLE DATA           Y   COPY public.quiz_responses (response_id, attempt_id, question_id, option_id) FROM stdin;
    public               postgres    false    246   _�       �          0    24804    quizzes 
   TABLE DATA           n   COPY public.quizzes (quiz_id, content_id, title, description, time_limit, created_at, updated_at) FROM stdin;
    public               postgres    false    238   |�       �          0    24786    submissions 
   TABLE DATA           l   COPY public.submissions (submission_id, assignment_id, user_id, file_path, submitted_at, grade) FROM stdin;
    public               postgres    false    236   ��       �          0    24636    users 
   TABLE DATA           �   COPY public.users (user_id, username, email, password_hash, role, created_at, last_login, last_login_ip, two_factor_enabled, two_factor_secret) FROM stdin;
    public               postgres    false    218   ��       �           0    0    agreements_agreement_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.agreements_agreement_id_seq', 1, false);
          public               postgres    false    249            �           0    0    applications_application_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.applications_application_id_seq', 1, false);
          public               postgres    false    223            �           0    0    assignments_assignment_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.assignments_assignment_id_seq', 1, false);
          public               postgres    false    233            �           0    0    content_content_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.content_content_id_seq', 1, false);
          public               postgres    false    231            �           0    0    enrollments_enrollment_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.enrollments_enrollment_id_seq', 1, false);
          public               postgres    false    227            �           0    0    messages_message_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.messages_message_id_seq', 1, false);
          public               postgres    false    247            �           0    0    modules_module_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.modules_module_id_seq', 1, false);
          public               postgres    false    229            �           0    0    payments_payment_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.payments_payment_id_seq', 1, false);
          public               postgres    false    225            �           0    0    profiles_profile_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.profiles_profile_id_seq', 1, false);
          public               postgres    false    219            �           0    0    programs_program_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.programs_program_id_seq', 1, false);
          public               postgres    false    221            �           0    0 !   progress_tracking_progress_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.progress_tracking_progress_id_seq', 1, false);
          public               postgres    false    251            �           0    0    quiz_attempts_attempt_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.quiz_attempts_attempt_id_seq', 1, false);
          public               postgres    false    243            �           0    0    quiz_options_option_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.quiz_options_option_id_seq', 1, false);
          public               postgres    false    241            �           0    0    quiz_questions_question_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.quiz_questions_question_id_seq', 1, false);
          public               postgres    false    239            �           0    0    quiz_responses_response_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.quiz_responses_response_id_seq', 1, false);
          public               postgres    false    245            �           0    0    quizzes_quiz_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.quizzes_quiz_id_seq', 1, false);
          public               postgres    false    237            �           0    0    submissions_submission_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.submissions_submission_id_seq', 1, false);
          public               postgres    false    235            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);
          public               postgres    false    217            �           2606    24918    agreements agreements_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.agreements
    ADD CONSTRAINT agreements_pkey PRIMARY KEY (agreement_id);
 D   ALTER TABLE ONLY public.agreements DROP CONSTRAINT agreements_pkey;
       public                 postgres    false    250            �           2606    24686    applications applications_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (application_id);
 H   ALTER TABLE ONLY public.applications DROP CONSTRAINT applications_pkey;
       public                 postgres    false    224            �           2606    24779    assignments assignments_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (assignment_id);
 F   ALTER TABLE ONLY public.assignments DROP CONSTRAINT assignments_pkey;
       public                 postgres    false    234            �           2606    24763    content content_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_pkey PRIMARY KEY (content_id);
 >   ALTER TABLE ONLY public.content DROP CONSTRAINT content_pkey;
       public                 postgres    false    232            �           2606    24726    enrollments enrollments_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (enrollment_id);
 F   ALTER TABLE ONLY public.enrollments DROP CONSTRAINT enrollments_pkey;
       public                 postgres    false    228            �           2606    24897    messages messages_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);
 @   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_pkey;
       public                 postgres    false    248            �           2606    24747    modules modules_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (module_id);
 >   ALTER TABLE ONLY public.modules DROP CONSTRAINT modules_pkey;
       public                 postgres    false    230            �           2606    24706    payments payments_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);
 @   ALTER TABLE ONLY public.payments DROP CONSTRAINT payments_pkey;
       public                 postgres    false    226            �           2606    24660    profiles profiles_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (profile_id);
 @   ALTER TABLE ONLY public.profiles DROP CONSTRAINT profiles_pkey;
       public                 postgres    false    220            �           2606    24676    programs programs_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.programs
    ADD CONSTRAINT programs_pkey PRIMARY KEY (program_id);
 @   ALTER TABLE ONLY public.programs DROP CONSTRAINT programs_pkey;
       public                 postgres    false    222            �           2606    24937 (   progress_tracking progress_tracking_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.progress_tracking
    ADD CONSTRAINT progress_tracking_pkey PRIMARY KEY (progress_id);
 R   ALTER TABLE ONLY public.progress_tracking DROP CONSTRAINT progress_tracking_pkey;
       public                 postgres    false    252            �           2606    24853     quiz_attempts quiz_attempts_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_pkey PRIMARY KEY (attempt_id);
 J   ALTER TABLE ONLY public.quiz_attempts DROP CONSTRAINT quiz_attempts_pkey;
       public                 postgres    false    244            �           2606    24841    quiz_options quiz_options_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.quiz_options
    ADD CONSTRAINT quiz_options_pkey PRIMARY KEY (option_id);
 H   ALTER TABLE ONLY public.quiz_options DROP CONSTRAINT quiz_options_pkey;
       public                 postgres    false    242            �           2606    24827 "   quiz_questions quiz_questions_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.quiz_questions
    ADD CONSTRAINT quiz_questions_pkey PRIMARY KEY (question_id);
 L   ALTER TABLE ONLY public.quiz_questions DROP CONSTRAINT quiz_questions_pkey;
       public                 postgres    false    240            �           2606    24870 "   quiz_responses quiz_responses_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_pkey PRIMARY KEY (response_id);
 L   ALTER TABLE ONLY public.quiz_responses DROP CONSTRAINT quiz_responses_pkey;
       public                 postgres    false    246            �           2606    24813    quizzes quizzes_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_pkey PRIMARY KEY (quiz_id);
 >   ALTER TABLE ONLY public.quizzes DROP CONSTRAINT quizzes_pkey;
       public                 postgres    false    238            �           2606    24792    submissions submissions_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (submission_id);
 F   ALTER TABLE ONLY public.submissions DROP CONSTRAINT submissions_pkey;
       public                 postgres    false    236            �           2606    24649    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    218            �           2606    24645    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    218            �           2606    24647    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    218            �           2606    24924 %   agreements agreements_program_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.agreements
    ADD CONSTRAINT agreements_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(program_id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.agreements DROP CONSTRAINT agreements_program_id_fkey;
       public               postgres    false    222    4802    250            �           2606    24919 "   agreements agreements_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.agreements
    ADD CONSTRAINT agreements_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.agreements DROP CONSTRAINT agreements_user_id_fkey;
       public               postgres    false    218    250    4796            �           2606    24692 )   applications applications_program_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(program_id) ON DELETE CASCADE;
 S   ALTER TABLE ONLY public.applications DROP CONSTRAINT applications_program_id_fkey;
       public               postgres    false    4802    222    224            �           2606    24687 &   applications applications_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.applications DROP CONSTRAINT applications_user_id_fkey;
       public               postgres    false    218    4796    224            �           2606    24780 '   assignments assignments_content_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(content_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.assignments DROP CONSTRAINT assignments_content_id_fkey;
       public               postgres    false    232    4812    234            �           2606    24764    content content_module_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(module_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.content DROP CONSTRAINT content_module_id_fkey;
       public               postgres    false    4810    232    230            �           2606    24732 '   enrollments enrollments_program_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(program_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.enrollments DROP CONSTRAINT enrollments_program_id_fkey;
       public               postgres    false    222    4802    228            �           2606    24727 $   enrollments enrollments_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.enrollments DROP CONSTRAINT enrollments_user_id_fkey;
       public               postgres    false    228    4796    218            �           2606    24903 #   messages messages_recipient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 M   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_recipient_id_fkey;
       public               postgres    false    248    4796    218            �           2606    24898     messages messages_sender_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_sender_id_fkey;
       public               postgres    false    218    248    4796            �           2606    24748    modules modules_program_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(program_id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.modules DROP CONSTRAINT modules_program_id_fkey;
       public               postgres    false    230    222    4802            �           2606    24712 !   payments payments_program_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.programs(program_id) ON DELETE CASCADE;
 K   ALTER TABLE ONLY public.payments DROP CONSTRAINT payments_program_id_fkey;
       public               postgres    false    222    4802    226            �           2606    24707    payments payments_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.payments DROP CONSTRAINT payments_user_id_fkey;
       public               postgres    false    4796    226    218            �           2606    24661    profiles profiles_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.profiles DROP CONSTRAINT profiles_user_id_fkey;
       public               postgres    false    4796    218    220            �           2606    24943 3   progress_tracking progress_tracking_content_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progress_tracking
    ADD CONSTRAINT progress_tracking_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(content_id) ON DELETE CASCADE;
 ]   ALTER TABLE ONLY public.progress_tracking DROP CONSTRAINT progress_tracking_content_id_fkey;
       public               postgres    false    252    4812    232            �           2606    24938 0   progress_tracking progress_tracking_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progress_tracking
    ADD CONSTRAINT progress_tracking_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.progress_tracking DROP CONSTRAINT progress_tracking_user_id_fkey;
       public               postgres    false    4796    252    218            �           2606    24854 (   quiz_attempts quiz_attempts_quiz_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(quiz_id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.quiz_attempts DROP CONSTRAINT quiz_attempts_quiz_id_fkey;
       public               postgres    false    4818    244    238            �           2606    24859 (   quiz_attempts quiz_attempts_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.quiz_attempts DROP CONSTRAINT quiz_attempts_user_id_fkey;
       public               postgres    false    218    244    4796            �           2606    24842 *   quiz_options quiz_options_question_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_options
    ADD CONSTRAINT quiz_options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.quiz_questions(question_id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.quiz_options DROP CONSTRAINT quiz_options_question_id_fkey;
       public               postgres    false    4820    240    242            �           2606    24828 *   quiz_questions quiz_questions_quiz_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_questions
    ADD CONSTRAINT quiz_questions_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(quiz_id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.quiz_questions DROP CONSTRAINT quiz_questions_quiz_id_fkey;
       public               postgres    false    238    4818    240            �           2606    24871 -   quiz_responses quiz_responses_attempt_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.quiz_attempts(attempt_id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.quiz_responses DROP CONSTRAINT quiz_responses_attempt_id_fkey;
       public               postgres    false    4824    246    244            �           2606    24881 ,   quiz_responses quiz_responses_option_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_option_id_fkey FOREIGN KEY (option_id) REFERENCES public.quiz_options(option_id) ON DELETE CASCADE;
 V   ALTER TABLE ONLY public.quiz_responses DROP CONSTRAINT quiz_responses_option_id_fkey;
       public               postgres    false    242    246    4822            �           2606    24876 .   quiz_responses quiz_responses_question_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quiz_responses
    ADD CONSTRAINT quiz_responses_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.quiz_questions(question_id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.quiz_responses DROP CONSTRAINT quiz_responses_question_id_fkey;
       public               postgres    false    240    246    4820            �           2606    24814    quizzes quizzes_content_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(content_id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.quizzes DROP CONSTRAINT quizzes_content_id_fkey;
       public               postgres    false    4812    232    238            �           2606    24793 *   submissions submissions_assignment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_assignment_id_fkey FOREIGN KEY (assignment_id) REFERENCES public.assignments(assignment_id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.submissions DROP CONSTRAINT submissions_assignment_id_fkey;
       public               postgres    false    234    236    4814            �           2606    24798 $   submissions submissions_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.submissions DROP CONSTRAINT submissions_user_id_fkey;
       public               postgres    false    218    4796    236            �           0    24754    content    ROW SECURITY     5   ALTER TABLE public.content ENABLE ROW LEVEL SECURITY;          public               postgres    false    232            �           0    24651    profiles    ROW SECURITY     6   ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;          public               postgres    false    220            �           0    24786    submissions    ROW SECURITY     9   ALTER TABLE public.submissions ENABLE ROW LEVEL SECURITY;          public               postgres    false    236            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     