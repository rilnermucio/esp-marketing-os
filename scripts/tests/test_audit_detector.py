"""Tests for audit_detector.py (input type detection)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from audit_detector import detect


class TestLandingDetection:
    def test_https_url(self):
        result = detect("https://stripe.com")
        assert result["type"] == "landing"
        assert result["normalized"] == "https://stripe.com"
        assert result["slug"] == "stripe"

    def test_http_url(self):
        result = detect("http://example.com")
        assert result["type"] == "landing"
        assert result["normalized"] == "http://example.com"

    def test_url_with_path(self):
        result = detect("https://example.com/landing")
        assert result["type"] == "landing"
        assert result["slug"] == "example"

    def test_url_with_trailing_slash(self):
        result = detect("https://stripe.com/")
        assert result["normalized"] == "https://stripe.com"

    def test_url_with_subdomain(self):
        result = detect("https://blog.stripe.com")
        assert result["slug"] == "stripe"

    def test_url_with_query_preserves_query(self):
        result = detect("https://stripe.com/?ref=1")
        assert result["normalized"] == "https://stripe.com/?ref=1"
        assert result["slug"] == "stripe"


class TestInstagramDetection:
    def test_at_prefix(self):
        result = detect("@ericorocha")
        assert result["type"] == "instagram"
        assert result["normalized"] == "ericorocha"
        assert result["slug"] == "ericorocha"

    def test_no_prefix_letters_only(self):
        result = detect("ericorocha")
        assert result["type"] == "instagram"
        assert result["normalized"] == "ericorocha"

    def test_with_dot(self):
        result = detect("@joao.silva")
        assert result["type"] == "instagram"
        assert result["normalized"] == "joao.silva"

    def test_with_underscore(self):
        result = detect("@user_name_123")
        assert result["type"] == "instagram"
        assert result["normalized"] == "user_name_123"

    def test_uppercase_lowercased(self):
        result = detect("@EricoRocha")
        assert result["normalized"] == "ericorocha"
        assert result["slug"] == "ericorocha"


class TestMetaAdsDetection:
    def test_meta_ad_library(self):
        result = detect("https://www.facebook.com/ads/library/?id=12345")
        assert result["type"] == "meta_ads"
        assert "facebook.com/ads/library" in result["normalized"]

    def test_meta_ads_pt_locale(self):
        result = detect(
            "https://www.facebook.com/ads/library/?country=BR&search_type=keyword&q=curso"
        )
        assert result["type"] == "meta_ads"


class TestYouTubeDetection:
    def test_full_url(self):
        result = detect("https://youtube.com/watch?v=dQw4w9WgXcQ")
        assert result["type"] == "youtube"
        assert result["slug"] == "dQw4w9WgXcQ"

    def test_short_url(self):
        result = detect("https://youtu.be/dQw4w9WgXcQ")
        assert result["type"] == "youtube"
        assert result["slug"] == "dQw4w9WgXcQ"

    def test_channel_url(self):
        result = detect("https://youtube.com/@channelname")
        assert result["type"] == "youtube"
        assert result["slug"] == "channelname"
