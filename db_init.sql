--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.0

-- Started on 2022-03-15 13:54:30 CET

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

--
-- TOC entry 3593 (class 1262 OID 33002)
-- Name: blackbird; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE blackbird WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';


ALTER DATABASE blackbird OWNER TO postgres;

\connect blackbird

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
-- TOC entry 211 (class 1259 OID 33017)
-- Name: annontate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annontate (
    id integer NOT NULL,
    date character varying(150),
    user_email character varying(150),
    data character varying(150),
    audio_name character varying(150)
);


ALTER TABLE public.annontate OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 33074)
-- Name: annontate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE TABLE public.annontate ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.annontate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 33010)
-- Name: birdsound; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.birdsound (
    id integer NOT NULL,
    audio_name character varying(150)[]
);


ALTER TABLE public.birdsound OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 33003)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(150) NOT NULL,
    password character varying(150),
    first_name character varying(150)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 33053)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."user" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3447 (class 2606 OID 33023)
-- Name: annontate Annotate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annontate
    ADD CONSTRAINT "Annotate_pkey" PRIMARY KEY (id);


--
-- TOC entry 3445 (class 2606 OID 33016)
-- Name: birdsound BirdSound_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.birdsound
    ADD CONSTRAINT "BirdSound_pkey" PRIMARY KEY (id);


--
-- TOC entry 3441 (class 2606 OID 33009)
-- Name: user User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 3443 (class 2606 OID 33068)
-- Name: user email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT email_unique UNIQUE (email);


--
-- TOC entry 3448 (class 2606 OID 33069)
-- Name: annontate email; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annontate
    ADD CONSTRAINT email FOREIGN KEY (user_email) REFERENCES public."user"(email) NOT VALID;


-- Completed on 2022-03-15 13:54:31 CET

--
-- PostgreSQL database dump complete
--

