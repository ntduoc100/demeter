using System.Data;
using System.Data.SqlClient;
using DemeterWeather.Models;
using System.Configuration;
using System.Collections.Generic;

namespace DemeterProject.Data

{
    public class db
    {
        SqlConnection conn = new SqlConnection("Data Source=(localdb)\\MSSQLLocalDB;Initial Catalog=DemeterProject;Integrated Security=True;Connect Timeout=30;Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False");

        // get Country List by Prefix
        public List<LocationList> LocationGet(string prefix)
        {
            List<LocationList> list = new List<LocationList>();
            SqlCommand com = new SqlCommand("Sp_Location", conn);
            com.CommandType = CommandType.StoredProcedure;
            com.Parameters.AddWithValue("@Prefix", prefix);
            SqlDataAdapter da = new SqlDataAdapter(com);
            DataSet ds = new DataSet();
            da.Fill(ds);
            foreach (DataRow dr in ds.Tables[0].Rows)
            {
                list.Add(new LocationList
                {
                    label = dr["LocationName"].ToString(),
                    val = dr["LocationID"].ToString()
                });
            }
            return list;
        }
    }
}
