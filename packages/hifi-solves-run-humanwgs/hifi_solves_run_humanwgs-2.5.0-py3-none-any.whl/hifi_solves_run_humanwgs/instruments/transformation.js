(context) => {
  if (!context.samples) {
    throw new Error('Samples are required for this transformation');
  }
  if (context.workflow_params['HumanWGS_wrapper.family']?.samples?.length > 0) {
    return {}
  }

  const backend = context.workflow_params['HumanWGS_wrapper.backend'];

  return {
    workflow_params: {
      'HumanWGS_wrapper.family': {
        family_id: context.workflow_params['HumanWGS_wrapper.family']?.family_id ?? context.samples.map(item => item.id).sort().join('__'),
        samples: context.samples?.map(sample => {
          return {
            sample_id: sample.id,
            hifi_reads: sample.files.map(sampleFile => {

              if (backend === "Azure") {
                let uri = sampleFile.path;
                // Remove the "https://" prefix
                if (uri.startsWith("https://")) {
                  uri = uri.slice(8);
                }

                // Split by "/" to extract components
                const parts = uri.split("/");

                // Extract storage account from the first part (hostname)
                const storageAccount = parts[0].split(".")[0];

                // The rest are: container and path
                const container = parts[1];
                const pathParts = parts.slice(2).join("/");

                // Construct the result
                return "/" + storageAccount + "/" + container + "/" + pathParts;
              } else {
                return sampleFile.path;
              }
            }),
            father_id: sample.father_id ?? "unknown",
            mother_id: sample.mother_id ?? "unknown",
            sex: sample.sex ?? "unknown",
            affected: sample.affected ?? false
          }
        }),
      },
    }
  }
}
