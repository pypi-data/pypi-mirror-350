from unittest.mock import patch, MagicMock
from rettxmutation.analysis.text_analytics import HealthcareTextAnalyzer


@patch("rettxmutation.analysis.text_analytics.TextAnalyticsClient")
def test_analyze_text_success(mock_client_class):
    """
    Test that analyze_text returns the first non-error doc from the poller.
    """

    # 1) Create a fake "healthcare document" object with no errors.
    #    In the actual SDK, you might get a HealthcareEntitiesResult or similar.
    fake_doc = MagicMock()
    fake_doc.is_error = False
    fake_doc.entities = []  # e.g., no entities for now
    fake_doc.entity_relations = []

    # 2) The poller.result() should return a list of documents. We have only one.
    mock_poller = MagicMock()
    mock_poller.result.return_value = [fake_doc]

    # 3) The text analytics client returns this poller
    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_healthcare_entities.return_value = mock_poller
    mock_client_class.return_value = mock_client_instance

    # 4) Instantiate your class
    analyzer = HealthcareTextAnalyzer(endpoint="https://dummy_endpoint", key="dummy_key")

    # 5) Call the method under test
    text_result = analyzer.analyze_text("some sample text")

    # 6) Verify
    assert text_result is not None
    assert text_result == fake_doc  # because docs[0] = fake_doc
    # Also ensure the correct client method is called
    mock_client_instance.begin_analyze_healthcare_entities.assert_called_once_with(["some sample text"])


@patch("rettxmutation.analysis.text_analytics.TextAnalyticsClient")
def test_analyze_text_no_valid_docs(mock_client_class, caplog):
    """
    If all docs are errors (or the poller returns an empty list),
    analyze_text should log an error and return None.
    """
    # Mock a doc that is_error = True
    fake_doc_error = MagicMock(is_error=True)

    mock_poller = MagicMock()
    mock_poller.result.return_value = [fake_doc_error]

    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_healthcare_entities.return_value = mock_poller
    mock_client_class.return_value = mock_client_instance

    analyzer = HealthcareTextAnalyzer("endpoint", "key")

    result = analyzer.analyze_text("bad text")
    assert result is None

    # Check logs if you wish
    assert "No valid documents found" in caplog.text


@patch("rettxmutation.analysis.text_analytics.TextAnalyticsClient")
def test_extract_variant_information(mock_client_class):
    """
    Test extract_variant_information picks up 'Variant' entities above the confidence threshold.
    """
    # 1) Create mock doc with multiple entities
    variant_entity = MagicMock(
        category="Variant",
        text="BRCA1 mutation",
        confidence_score=0.85
    )
    low_conf_variant = MagicMock(
        category="Variant",
        text="Uncertain mutation",
        confidence_score=0.2
    )
    gene_entity = MagicMock(
        category="GeneOrProtein",
        text="BRCA1",
        confidence_score=0.9
    )

    fake_doc = MagicMock()
    fake_doc.is_error = False
    fake_doc.entities = [variant_entity, low_conf_variant, gene_entity]
    fake_doc.entity_relations = []

    mock_poller = MagicMock()
    mock_poller.result.return_value = [fake_doc]

    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_healthcare_entities.return_value = mock_poller
    mock_client_class.return_value = mock_client_instance

    analyzer = HealthcareTextAnalyzer("endpoint", "key")

    # 2) First, call analyze_text (just to mimic the normal flow)
    doc = analyzer.analyze_text("BRCA text...")

    # 3) Then, call extract_variant_information
    #    We set confidence_threshold=0.5, so the second variant (0.2) should be excluded
    variants = analyzer.extract_variant_information(doc, confidence_threshold=0.5)
    assert len(variants) == 1
    first_variant = variants[0]
    assert first_variant.value == "BRCA1 mutation"
    assert first_variant.type == "variant"
    assert first_variant.confidence == 0.85


@patch("rettxmutation.analysis.text_analytics.TextAnalyticsClient")
def test_extract_variant_information_empty_doc(mock_client_class):
    """
    If the doc is None or empty, extract_variant_information returns an empty list.
    """
    analyzer = HealthcareTextAnalyzer("endpoint", "key")

    # Pass None
    variants_none = analyzer.extract_variant_information(None)
    assert variants_none == []

    # Pass mock doc without entities
    fake_doc = MagicMock()
    fake_doc.entities = []
    result = analyzer.extract_variant_information(fake_doc)
    assert result == []


@patch("rettxmutation.analysis.text_analytics.TextAnalyticsClient")
def test_extract_genetic_information(mock_client_class):
    """
    Test extracting variants, genes, mutation types, and relations.
    """
    # 1) Create some mock entities
    var_entity = MagicMock(
        category="Variant",
        text="BRCA2 c.9976A>T",
        normalized_text="BRCA2 c.9976A>T",
        confidence_score=0.92
    )
    gene_entity = MagicMock(
        category="GeneOrProtein",
        text="BRCA2",
        normalized_text="BRCA2",
        confidence_score=0.95
    )
    mut_type_entity = MagicMock(
        category="MutationType",
        text="Missense mutation",
        normalized_text="Missense",
        confidence_score=0.88
    )

    # 2) Create a mock relation that references these roles
    # Typically 'roles' is a list of object references to these entities
    # We'll create MagicMock for roles
    rel_mock = MagicMock()
    rel_mock.relation_type = "some_relation"
    role1 = MagicMock(name="role1")  # This labels the mock object internally
    role1.entity = var_entity
    role1.name = "mutation"         # This is the property your code uses

    role2 = MagicMock(name="role2")  # This labels the mock object
    role2.entity = gene_entity
    role2.name = "gene"

    rel_mock.roles = [role1, role2]

    fake_doc = MagicMock()
    fake_doc.is_error = False
    fake_doc.entities = [var_entity, gene_entity, mut_type_entity]
    fake_doc.entity_relations = [rel_mock]

    # poller -> result -> [fake_doc]
    mock_poller = MagicMock()
    mock_poller.result.return_value = [fake_doc]
    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_healthcare_entities.return_value = mock_poller
    mock_client_class.return_value = mock_client_instance

    analyzer = HealthcareTextAnalyzer("endpoint", "key")
    doc = analyzer.analyze_text("some text about BRCA2")

    # 3) Now call extract_genetic_information
    data = analyzer.extract_genetic_information(doc)

    assert "variants" in data
    assert len(data["variants"]) == 1
    assert data["variants"][0]["text"] == "BRCA2 c.9976A>T"

    assert "genes" in data
    assert len(data["genes"]) == 1
    assert data["genes"][0]["text"] == "BRCA2"

    assert "mutation_types" in data
    assert len(data["mutation_types"]) == 1
    assert data["mutation_types"][0]["text"] == "Missense mutation"

    # Check relation
    assert "relations" in data
    assert len(data["relations"]) == 1
    rel_info = data["relations"][0]
    assert rel_info["relation_type"] == "some_relation"
    assert len(rel_info["roles"]) == 2
    assert rel_info["roles"][0]["entity_text"] == "BRCA2 c.9976A>T"
    assert rel_info["roles"][1]["entity_text"] == "BRCA2"

    # 4) Finally call extract_genetic_information with None
    empty_data = analyzer.extract_genetic_information(None)
    assert empty_data == {
        "variants": [],
        "genes": [],
        "mutation_types": [],
        "relations": []
    }
