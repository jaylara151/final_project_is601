def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "IS601 Calculator History App" in response.text


def test_full_website_workflow(client):
    create_response = client.post(
        "/calculate",
        data={
            "first_number": "20",
            "second_number": "4",
            "operation": "divide",
            "note": "e2e test note",
        },
        follow_redirects=True,
    )

    assert create_response.status_code == 200
    assert "Calculation History" in create_response.text
    assert "e2e test note" in create_response.text

    history_response = client.get("/history")

    assert history_response.status_code == 200
    assert "20.0" in history_response.text
    assert "divide" in history_response.text
    assert "4.0" in history_response.text
    assert "5.0" in history_response.text

    detail_response = client.get("/history/1")

    assert detail_response.status_code == 200
    assert "Calculation Details" in detail_response.text
    assert "divide" in detail_response.text

    update_response = client.post(
        "/history/1/edit",
        data={
            "note": "updated e2e note",
        },
        follow_redirects=True,
    )

    assert update_response.status_code == 200
    assert "updated e2e note" in update_response.text

    report_response = client.get("/reports")

    assert report_response.status_code == 200
    assert "Summary Report" in report_response.text
    assert "Total Calculations" in report_response.text

    delete_response = client.post(
        "/history/1/delete",
        follow_redirects=True,
    )

    assert delete_response.status_code == 200
    assert "updated e2e note" not in delete_response.text