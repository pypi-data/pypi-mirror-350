"""
StartGarlic - A RAG-based Contextual Ad Integration System

StartGarlic empowers LLM applications to seamlessly integrate contextual advertisements,
enabling startups to monetize their AI-driven products effectively. The system uses
RAG (Retrieval Augmented Generation) to ensure ads are relevant and non-intrusive.

Key Features:
- Contextual ad placement in AI responses
- Real-time bidding and auction system
- Analytics and performance tracking
- Easy SDK integration
"""

__version__ = "0.1.19"

from .core import Garlic

__all__ = ["Garlic"]