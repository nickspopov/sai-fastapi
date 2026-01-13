--
-- PostgreSQL database dump
--

\restrict PX9nJmnnP3nLvV3hG3exPFaa4mqfE5GeqfEYrie1IpSu4f2js92ltHbdhA88fRZ

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: calendarevent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendarevent (
    id character varying NOT NULL,
    title character varying NOT NULL,
    notes character varying NOT NULL,
    started_at timestamp without time zone NOT NULL,
    ended_at timestamp without time zone NOT NULL,
    event_type character varying NOT NULL,
    user_id character varying NOT NULL
);


ALTER TABLE public.calendarevent OWNER TO postgres;

--
-- Name: calendareventjob; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendareventjob (
    id character varying NOT NULL,
    calendar_event_id character varying NOT NULL,
    user_id character varying NOT NULL,
    scheduled_at timestamp without time zone NOT NULL
);


ALTER TABLE public.calendareventjob OWNER TO postgres;

--
-- Name: community; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.community (
    id character varying NOT NULL,
    name character varying NOT NULL,
    owner_id character varying NOT NULL
);


ALTER TABLE public.community OWNER TO postgres;

--
-- Name: communitycheckinjob; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communitycheckinjob (
    id character varying NOT NULL,
    community_id character varying NOT NULL,
    member_id character varying NOT NULL,
    scheduled_at timestamp without time zone NOT NULL
);


ALTER TABLE public.communitycheckinjob OWNER TO postgres;

--
-- Name: communitymember; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communitymember (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    community_id character varying NOT NULL,
    last_checkin timestamp without time zone
);


ALTER TABLE public.communitymember OWNER TO postgres;

--
-- Name: communityplace; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communityplace (
    id character varying NOT NULL,
    name character varying NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    community_id character varying NOT NULL
);


ALTER TABLE public.communityplace OWNER TO postgres;

--
-- Name: dog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dog (
    id character varying NOT NULL,
    name character varying NOT NULL,
    breed character varying NOT NULL,
    date_of_birth timestamp without time zone NOT NULL,
    sex character varying NOT NULL
);


ALTER TABLE public.dog OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id character varying NOT NULL,
    email character varying NOT NULL,
    name character varying NOT NULL,
    push_tokens json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    language character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: userdog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userdog (
    user_id character varying NOT NULL,
    dog_id character varying NOT NULL
);


ALTER TABLE public.userdog OWNER TO postgres;

--
-- Name: walk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.walk (
    id character varying NOT NULL,
    started_at timestamp without time zone NOT NULL,
    finished_at timestamp without time zone NOT NULL,
    user_id character varying NOT NULL
);


ALTER TABLE public.walk OWNER TO postgres;

--
-- Name: walkinterval; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.walkinterval (
    id character varying NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    walk_id character varying NOT NULL
);


ALTER TABLE public.walkinterval OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
bfb8d5639915
\.


--
-- Data for Name: calendarevent; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calendarevent (id, title, notes, started_at, ended_at, event_type, user_id) FROM stdin;
\.


--
-- Data for Name: calendareventjob; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calendareventjob (id, calendar_event_id, user_id, scheduled_at) FROM stdin;
\.


--
-- Data for Name: community; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community (id, name, owner_id) FROM stdin;
\.


--
-- Data for Name: communitycheckinjob; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communitycheckinjob (id, community_id, member_id, scheduled_at) FROM stdin;
\.


--
-- Data for Name: communitymember; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communitymember (id, user_id, community_id, last_checkin) FROM stdin;
\.


--
-- Data for Name: communityplace; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communityplace (id, name, latitude, longitude, community_id) FROM stdin;
\.


--
-- Data for Name: dog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dog (id, name, breed, date_of_birth, sex) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, name, push_tokens, created_at, updated_at, language) FROM stdin;
default_user	dev@example.com	Default User	{}	2026-01-13 20:18:52.896184	2026-01-13 20:18:52.896184	en
\.


--
-- Data for Name: userdog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userdog (user_id, dog_id) FROM stdin;
\.


--
-- Data for Name: walk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.walk (id, started_at, finished_at, user_id) FROM stdin;
\.


--
-- Data for Name: walkinterval; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.walkinterval (id, latitude, longitude, "timestamp", walk_id) FROM stdin;
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: calendarevent calendarevent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendarevent
    ADD CONSTRAINT calendarevent_pkey PRIMARY KEY (id);


--
-- Name: calendareventjob calendareventjob_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendareventjob
    ADD CONSTRAINT calendareventjob_pkey PRIMARY KEY (id);


--
-- Name: community community_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.community
    ADD CONSTRAINT community_pkey PRIMARY KEY (id);


--
-- Name: communitycheckinjob communitycheckinjob_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitycheckinjob
    ADD CONSTRAINT communitycheckinjob_pkey PRIMARY KEY (id);


--
-- Name: communitymember communitymember_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitymember
    ADD CONSTRAINT communitymember_pkey PRIMARY KEY (id);


--
-- Name: communityplace communityplace_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communityplace
    ADD CONSTRAINT communityplace_pkey PRIMARY KEY (id);


--
-- Name: dog dog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dog
    ADD CONSTRAINT dog_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: userdog userdog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdog
    ADD CONSTRAINT userdog_pkey PRIMARY KEY (user_id, dog_id);


--
-- Name: walk walk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.walk
    ADD CONSTRAINT walk_pkey PRIMARY KEY (id);


--
-- Name: walkinterval walkinterval_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.walkinterval
    ADD CONSTRAINT walkinterval_pkey PRIMARY KEY (id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: calendarevent calendarevent_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendarevent
    ADD CONSTRAINT calendarevent_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: calendareventjob calendareventjob_calendar_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendareventjob
    ADD CONSTRAINT calendareventjob_calendar_event_id_fkey FOREIGN KEY (calendar_event_id) REFERENCES public.calendarevent(id);


--
-- Name: calendareventjob calendareventjob_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendareventjob
    ADD CONSTRAINT calendareventjob_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: community community_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.community
    ADD CONSTRAINT community_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: communitycheckinjob communitycheckinjob_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitycheckinjob
    ADD CONSTRAINT communitycheckinjob_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: communitycheckinjob communitycheckinjob_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitycheckinjob
    ADD CONSTRAINT communitycheckinjob_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.communitymember(id);


--
-- Name: communitymember communitymember_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitymember
    ADD CONSTRAINT communitymember_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: communitymember communitymember_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communitymember
    ADD CONSTRAINT communitymember_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: communityplace communityplace_community_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communityplace
    ADD CONSTRAINT communityplace_community_id_fkey FOREIGN KEY (community_id) REFERENCES public.community(id);


--
-- Name: userdog userdog_dog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdog
    ADD CONSTRAINT userdog_dog_id_fkey FOREIGN KEY (dog_id) REFERENCES public.dog(id);


--
-- Name: userdog userdog_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userdog
    ADD CONSTRAINT userdog_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: walk walk_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.walk
    ADD CONSTRAINT walk_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: walkinterval walkinterval_walk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.walkinterval
    ADD CONSTRAINT walkinterval_walk_id_fkey FOREIGN KEY (walk_id) REFERENCES public.walk(id);


--
-- PostgreSQL database dump complete
--

\unrestrict PX9nJmnnP3nLvV3hG3exPFaa4mqfE5GeqfEYrie1IpSu4f2js92ltHbdhA88fRZ

