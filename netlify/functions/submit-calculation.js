const { Pool } = require('pg');

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  // Parse the request body
  let data;
  try {
    data = JSON.parse(event.body);
  } catch (e) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Invalid JSON' })
    };
  }

  // Connect to Neon database
  const pool = new Pool({
    connectionString: process.env.NEON_DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });

  try {
    const query = `
      INSERT INTO calculator_submissions (
        project_name,
        state,
        contract_value,
        labor_scope,
        payroll,
        sub_amount,
        sub_name,
        sub_contact_name,
        sub_contact_email,
        wc_amount,
        gl_amount,
        umbrella_amount,
        include_op,
        op_amount,
        total_deduction,
        submitted_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, NOW())
      RETURNING id
    `;

    const values = [
      data.projectName || '',
      data.state || '',
      data.contractValue || 0,
      data.laborScope || 'none',
      data.payroll || 0,
      data.subAmount || 0,
      data.subName || '',
      data.subContactName || '',
      data.subContactEmail || '',
      data.wcAmount || 0,
      data.glAmount || 0,
      data.umbrellaAmount || 0,
      data.includeOP || false,
      data.opAmount || 0,
      data.totalDeduction || 0
    ];

    const result = await pool.query(query, values);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        message: 'Submission saved successfully',
        id: result.rows[0].id
      })
    };

  } catch (error) {
    console.error('Database error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to save submission' })
    };
  } finally {
    await pool.end();
  }
};
