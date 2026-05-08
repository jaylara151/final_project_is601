def test_create_calculation(client):
    response = client.post(
        "/calculations/",
        json={
            "first_number": 10,
            "second_number": 5,
            "operation": "add",
            "note": "integration test",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["first_number"] == 10
    assert data["second_number"] == 5
    assert data["operation"] == "add"
    assert data["result"] == 15
    assert data["note"] == "integration test"


def test_get_all_calculations(client):
    client.post(
        "/calculations/",
        json={
            "first_number": 20,
            "second_number": 4,
            "operation": "divide",
            "note": "saved test",
        },
    )

    response = client.get("/calculations/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["result"] == 5


def test_get_one_calculation(client):
    create_response = client.post(
        "/calculations/",
        json={
            "first_number": 7,
            "second_number": 3,
            "operation": "add",
            "note": "one calculation",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.get(f"/calculations/{calculation_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == calculation_id
    assert data["result"] == 10


def test_update_calculation_note(client):
    create_response = client.post(
        "/calculations/",
        json={
            "first_number": 8,
            "second_number": 2,
            "operation": "multiply",
            "note": "old note",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        json={
            "note": "new note",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["note"] == "new note"


def test_delete_calculation(client):
    create_response = client.post(
        "/calculations/",
        json={
            "first_number": 9,
            "second_number": 3,
            "operation": "divide",
            "note": "delete this",
        },
    )

    calculation_id = create_response.json()["id"]

    delete_response = client.delete(f"/calculations/{calculation_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Calculation deleted successfully."

    get_response = client.get(f"/calculations/{calculation_id}")

    assert get_response.status_code == 404


def test_report_summary(client):
    client.post(
        "/calculations/",
        json={
            "first_number": 10,
            "second_number": 5,
            "operation": "add",
            "note": "first report test",
        },
    )

    client.post(
        "/calculations/",
        json={
            "first_number": 20,
            "second_number": 4,
            "operation": "divide",
            "note": "second report test",
        },
    )

    response = client.get("/calculations/report/summary")
    data = response.json()

    assert response.status_code == 200
    assert data["total_calculations"] == 2
    assert data["highest_result"] == 15
    assert data["lowest_result"] == 5
    assert data["most_common_operation"] is not None